<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">知识问答</h1>

    <div class="bg-white rounded-xl shadow-sm p-4 md:p-6">
      <p class="text-sm text-gray-600 mb-4">
        输入问题即可开始对话。系统会优先结合知识库内容回答；若暂无知识内容，则由 AI 直接给出建议。
      </p>

      <div class="h-[60vh] overflow-y-auto bg-gray-50 rounded-lg p-4 space-y-3">
        <div v-if="messages.length === 0" class="text-sm text-gray-500 text-center py-8">
          还没有对话，试试问：维修员接单后该怎么处理？
        </div>
        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="msg.role === 'user' ? 'flex justify-end' : 'flex justify-start'"
        >
          <div
            :class="[
              'max-w-[80%] rounded-2xl px-4 py-3 text-sm',
              msg.role === 'user'
                ? 'bg-primary text-white rounded-br-md'
                : 'bg-white text-gray-800 border border-gray-200 rounded-bl-md'
            ]"
          >
            <template v-if="msg.role === 'user'">
              <div class="whitespace-pre-wrap">{{ msg.content }}</div>
            </template>
            <template v-else>
              <div class="markdown-body" v-html="renderMarkdown(msg.content)"></div>
            </template>
            <div v-if="msg.role === 'assistant' && msg.sources?.length" class="mt-2 pt-2 border-t border-gray-200/70">
              <p class="text-xs text-gray-500 mb-1">参考来源：</p>
              <p class="text-xs text-gray-600">
                {{ msg.sources.map((s) => `【${s.category_display || s.category}】${s.title}`).join('；') }}
              </p>
            </div>
          </div>
        </div>
        <div v-if="asking" class="flex justify-start">
          <div class="bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 text-sm text-gray-500">
            AI 正在思考...
          </div>
        </div>
      </div>

      <div class="mt-4 flex gap-2">
        <textarea
          v-model="question"
          rows="2"
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          placeholder="输入你的问题..."
          @keydown.enter.exact.prevent="ask"
        />
        <button
          class="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed"
          :disabled="asking || !question.trim()"
          @click="ask"
        >
          发送
        </button>
      </div>
      <div v-if="error" class="text-sm text-red-600 mt-2">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { marked } from 'marked'

const question = ref('')
const messages = ref([])
const asking = ref(false)
const error = ref('')
let messageId = 0

async function ask() {
  if (!question.value.trim()) return
  const userQuestion = question.value.trim()
  question.value = ''
  messages.value.push({ id: ++messageId, role: 'user', content: userQuestion })
  const assistantMessage = { id: ++messageId, role: 'assistant', content: '', sources: [] }
  messages.value.push(assistantMessage)
  asking.value = true
  error.value = ''
  try {
    await askStream(userQuestion, assistantMessage)
  } catch (e) {
    const status = e?.response?.status
    if (e?.code === 'ECONNABORTED') {
      error.value = 'AI 响应超时，请稍后重试（可简化问题或减少并发请求）'
    } else if (status === 503) {
      error.value = e?.response?.data?.error || 'AI 服务暂时不可用，请稍后重试'
    } else if (status === 401) {
      error.value = '登录状态已失效，请重新登录后再提问'
    } else if (status === 403) {
      error.value = '你当前没有知识问答权限，请联系管理员'
    } else if (!e?.response && e?.request) {
      error.value = '请求未收到响应，请检查后端服务是否运行'
    } else {
      error.value = e?.response?.data?.error || e?.response?.data?.detail || '提问失败，请稍后重试'
    }
    assistantMessage.content = error.value
    assistantMessage.sources = []
  } finally {
    asking.value = false
  }
}

function renderMarkdown(text) {
  return marked.parse(text || '', { breaks: true })
}

function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split('; ') : []
  for (const cookie of cookies) {
    const [key, ...rest] = cookie.split('=')
    if (key === name) return decodeURIComponent(rest.join('='))
  }
  return ''
}

async function askStream(userQuestion, assistantMessage) {
  const response = await fetch('/api/knowledge/ask_stream/', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ question: userQuestion }),
  })

  if (!response.ok || !response.body) {
    const text = await response.text()
    throw new Error(text || `请求失败(${response.status})`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const chunks = buffer.split('\n\n')
    buffer = chunks.pop() || ''

    for (const chunk of chunks) {
      const lines = chunk.split('\n')
      let event = 'message'
      let dataLine = ''
      for (const line of lines) {
        if (line.startsWith('event:')) event = line.slice(6).trim()
        if (line.startsWith('data:')) dataLine += line.slice(5).trim()
      }
      if (!dataLine) continue

      let payload = {}
      try {
        payload = JSON.parse(dataLine)
      } catch {
        payload = {}
      }

      if (event === 'meta') {
        assistantMessage.sources = Array.isArray(payload.sources) ? payload.sources : []
      } else if (event === 'token') {
        assistantMessage.content += payload.token || ''
      } else if (event === 'error') {
        assistantMessage.content = payload.fallback || payload.error || '流式请求失败'
      }
    }
  }
}
</script>

<style scoped>
.markdown-body :deep(p) {
  margin: 0.25rem 0;
}
.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  margin: 0.25rem 0 0.25rem 1rem;
  padding-left: 1rem;
}
.markdown-body :deep(code) {
  background: #f3f4f6;
  padding: 0.1rem 0.3rem;
  border-radius: 0.25rem;
}
.markdown-body :deep(pre) {
  background: #111827;
  color: #f9fafb;
  border-radius: 0.5rem;
  padding: 0.75rem;
  overflow-x: auto;
}
</style>

