import json

from django.http import StreamingHttpResponse
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import KnowledgeItem, QALog, KnowledgeDocument
from .permissions import IsAdmin
from .serializers import (
    KnowledgeItemSerializer,
    AskKnowledgeSerializer,
    QALogSerializer,
    KnowledgeDocumentSerializer,
)
from .services.llm_service import (
    build_messages,
    chat_completion,
    chat_completion_stream,
    LLMServiceError,
)
from .services.document_parser import extract_text_from_file, DocumentParseError


def _user_role_scope(user):
    if user.is_student():
        return 'student'
    if user.is_repairman():
        return 'repairman'
    return 'all'


def _user_role_name(user):
    if user.is_student():
        return '学生'
    if user.is_repairman():
        return '维修人员'
    return '管理员'


def _build_prompt_and_sources(user):
    role_scope = _user_role_scope(user)
    role_name = _user_role_name(user)

    items = KnowledgeItem.objects.filter(
        is_active=True,
        role_scope__in=[role_scope, 'all'],
    ).order_by('-updated_at')[:20]
    context_lines = []
    sources = []
    for item in items:
        context_lines.append(f'[{item.get_category_display()}] 标题：{item.title}\n内容：{item.content}')
        sources.append({
            'id': item.id,
            'source_type': 'item',
            'title': item.title,
            'category': item.category,
            'category_display': item.get_category_display(),
        })

    if context_lines:
        system_prompt = (
            '你是 DormFix 宿舍报修系统的智能助手。'
            f'当前提问用户角色是：{role_name}。'
            '请优先参考提供的知识库内容回答，若知识库未覆盖，可结合通用常识补充，'
            '但必须明确标注“以下为通用建议”。回答要简洁、可执行。'
            '\n\n以下是知识库内容：\n'
            + '\n\n'.join(context_lines)
        )
    else:
        system_prompt = (
            '你是 DormFix 宿舍报修系统的智能助手。'
            f'当前提问用户角色是：{role_name}。'
            '当前没有可用的知识库上下文，请根据通用经验给出尽量稳妥、可执行的建议，'
            '并提醒用户以管理员发布规则为准。'
        )

    return role_name, system_prompt, sources


class KnowledgeItemViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeItem.objects.all()
    serializer_class = KnowledgeItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['updated_at', 'created_at']
    ordering = ['-updated_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def ask(self, request):
        serializer = AskKnowledgeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.validated_data['question'].strip()

        role_name, system_prompt, sources = _build_prompt_and_sources(request.user)

        try:
            answer = chat_completion(build_messages(system_prompt, question))
            QALog.objects.create(
                user=request.user,
                role=role_name,
                question=question,
                answer=answer,
                success=True,
            )
            return Response({'answer': answer, 'sources': sources[:5]})
        except LLMServiceError as e:
            fallback_answer = (
                '智能问答暂时不可用，请稍后重试。'
                '你也可以先查看系统公告或联系管理员。'
            )
            QALog.objects.create(
                user=request.user,
                role=role_name,
                question=question,
                answer=fallback_answer,
                success=False,
                error_message=str(e),
            )
            return Response(
                {'error': str(e), 'answer': fallback_answer, 'sources': sources[:5]},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def ask_stream(self, request):
        serializer = AskKnowledgeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.validated_data['question'].strip()
        role_name, system_prompt, sources = _build_prompt_and_sources(request.user)

        def event_stream():
            full_answer = ''
            try:
                meta_payload = json.dumps({'sources': sources[:5]}, ensure_ascii=False)
                yield f'event: meta\ndata: {meta_payload}\n\n'
                for token in chat_completion_stream(build_messages(system_prompt, question)):
                    full_answer += token
                    token_payload = json.dumps({'token': token}, ensure_ascii=False)
                    yield f'event: token\ndata: {token_payload}\n\n'

                QALog.objects.create(
                    user=request.user,
                    role=role_name,
                    question=question,
                    answer=full_answer.strip() or '',
                    success=True,
                )
                yield 'event: done\ndata: {"ok":true}\n\n'
            except LLMServiceError as e:
                fallback_answer = '智能问答暂时不可用，请稍后重试。你也可以先查看系统公告或联系管理员。'
                QALog.objects.create(
                    user=request.user,
                    role=role_name,
                    question=question,
                    answer=fallback_answer,
                    success=False,
                    error_message=str(e),
                )
                err_payload = json.dumps({'error': str(e), 'fallback': fallback_answer}, ensure_ascii=False)
                yield f'event: error\ndata: {err_payload}\n\n'
            except Exception as e:
                err_payload = json.dumps({'error': f'流式输出异常: {e}'}, ensure_ascii=False)
                yield f'event: error\ndata: {err_payload}\n\n'

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdmin])
    def qa_logs(self, request):
        logs = QALog.objects.all().order_by('-created_at')
        page = self.paginate_queryset(logs)
        if page is not None:
            serializer = QALogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = QALogSerializer(logs, many=True)
        return Response(serializer.data)


class KnowledgeDocumentViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeDocument.objects.all().order_by('-updated_at')
    serializer_class = KnowledgeDocumentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'original_filename']
    ordering_fields = ['updated_at', 'created_at']
    ordering = ['-updated_at']

    def perform_create(self, serializer):
        file_obj = self.request.FILES.get('file')
        if not file_obj:
            serializer.save(
                original_filename='',
                parse_status='failed',
                parse_error='缺少上传文件',
            )
            return

        instance = serializer.save(
            original_filename=file_obj.name,
            parse_status='pending',
            parse_error='',
        )
        self._parse_and_update(instance, file_obj)

    def perform_update(self, serializer):
        file_obj = self.request.FILES.get('file')
        instance = serializer.save()
        if file_obj:
            instance.original_filename = file_obj.name
            instance.parse_status = 'pending'
            instance.parse_error = ''
            instance.extracted_text = ''
            instance.save(update_fields=['original_filename', 'parse_status', 'parse_error', 'extracted_text', 'updated_at'])
            self._parse_and_update(instance, file_obj)

    @action(detail=True, methods=['post'])
    def reparse(self, request, pk=None):
        doc = self.get_object()
        if not doc.file:
            return Response({'error': '该文档没有可解析文件'}, status=status.HTTP_400_BAD_REQUEST)
        doc.parse_status = 'pending'
        doc.parse_error = ''
        doc.extracted_text = ''
        doc.save(update_fields=['parse_status', 'parse_error', 'extracted_text', 'updated_at'])
        self._parse_and_update(doc, doc.file)
        return Response(KnowledgeDocumentSerializer(doc).data)

    def _parse_and_update(self, instance, file_obj):
        try:
            file_obj.seek(0)
            text = extract_text_from_file(file_obj).strip()
            if not text:
                raise DocumentParseError('文件解析后内容为空')
            instance.extracted_text = text
            instance.parse_status = 'success'
            instance.parse_error = ''
        except DocumentParseError as e:
            instance.extracted_text = ''
            instance.parse_status = 'failed'
            instance.parse_error = str(e)
        except Exception as e:
            instance.extracted_text = ''
            instance.parse_status = 'failed'
            instance.parse_error = f'解析异常: {e}'
        instance.save(update_fields=['extracted_text', 'parse_status', 'parse_error', 'updated_at'])


