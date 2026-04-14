import json
import os
from urllib import request
from urllib.error import HTTPError, URLError


class LLMServiceError(Exception):
    pass


def build_messages(system_prompt: str, user_question: str):
    return [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_question},
    ]


def chat_completion(messages):
    api_key = os.environ.get('LLM_API_KEY', '').strip()
    if not api_key:
        raise LLMServiceError('LLM_API_KEY 未配置')

    base_url = os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1').rstrip('/')
    model = os.environ.get('LLM_MODEL', 'gpt-4o-mini')
    timeout = int(os.environ.get('LLM_TIMEOUT_SECONDS', '30'))

    payload = {
        'model': model,
        'messages': messages,
        'temperature': 0.2,
    }

    req = request.Request(
        f'{base_url}/chat/completions',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        method='POST',
    )

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except HTTPError as e:
        detail = e.read().decode('utf-8', errors='ignore') if e.fp else str(e)
        raise LLMServiceError(f'大模型接口调用失败: {detail}') from e
    except URLError as e:
        raise LLMServiceError(f'大模型接口连接失败: {e.reason}') from e
    except Exception as e:
        raise LLMServiceError(f'大模型响应解析失败: {e}') from e

    try:
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise LLMServiceError(f'大模型返回结构异常: {data}') from e


def chat_completion_stream(messages):
    api_key = os.environ.get('LLM_API_KEY', '').strip()
    if not api_key:
        raise LLMServiceError('LLM_API_KEY 未配置')

    base_url = os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1').rstrip('/')
    model = os.environ.get('LLM_MODEL', 'gpt-4o-mini')
    timeout = int(os.environ.get('LLM_TIMEOUT_SECONDS', '30'))

    payload = {
        'model': model,
        'messages': messages,
        'temperature': 0.2,
        'stream': True,
    }

    req = request.Request(
        f'{base_url}/chat/completions',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        method='POST',
    )

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            for raw_line in resp:
                line = raw_line.decode('utf-8', errors='ignore').strip()
                if not line or not line.startswith('data:'):
                    continue
                data_str = line[5:].strip()
                if data_str == '[DONE]':
                    break
                try:
                    payload = json.loads(data_str)
                except json.JSONDecodeError:
                    continue
                choices = payload.get('choices') or []
                if not choices:
                    continue
                delta = choices[0].get('delta') or {}
                token = delta.get('content')
                if token:
                    yield token
    except HTTPError as e:
        detail = e.read().decode('utf-8', errors='ignore') if e.fp else str(e)
        raise LLMServiceError(f'大模型接口调用失败: {detail}') from e
    except URLError as e:
        raise LLMServiceError(f'大模型接口连接失败: {e.reason}') from e
    except Exception as e:
        raise LLMServiceError(f'大模型流式响应失败: {e}') from e

