"""
健康检查视图
用于 Docker 健康检查和负载均衡器
"""
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    健康检查端点
    检查数据库连接和应用状态
    """
    try:
        # 检查数据库连接
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected'
        }, status=200)
    
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)


@csrf_exempt
@require_http_methods(["GET"])
def readiness_check(request):
    """
    就绪检查端点
    检查应用是否准备好接收流量
    """
    try:
        # 检查数据库连接
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # 可以添加更多检查，如缓存、消息队列等
        
        return JsonResponse({
            'status': 'ready',
            'checks': {
                'database': 'ok'
            }
        }, status=200)
    
    except Exception as e:
        return JsonResponse({
            'status': 'not_ready',
            'error': str(e)
        }, status=503)
