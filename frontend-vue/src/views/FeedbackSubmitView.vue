<template>
  <div>
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">反馈</h1>

    <div class="mb-6 flex gap-2">
      <button
        class="px-4 py-2 rounded-lg transition-colors cursor-pointer min-w-[112px] text-center"
        :class="activeTab === 'submit' ? 'bg-primary text-white' : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'"
        @click="switchTab('submit')"
      >
        提交反馈
      </button>
      <button
        class="px-4 py-2 rounded-lg transition-colors cursor-pointer relative min-w-[112px] text-center"
        :class="activeTab === 'records' ? 'bg-primary text-white' : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'"
        @click="switchTab('records')"
      >
        反馈记录
        <span
          v-if="unreadCount > 0"
          class="absolute top-1 right-2 min-w-[18px] h-[18px] px-1 bg-red-500 text-white text-[10px] leading-[18px] rounded-full text-center"
        >
          {{ unreadCount > 99 ? '99+' : unreadCount }}
        </span>
      </button>
    </div>

    <div v-if="activeTab === 'submit'" class="max-w-2xl">
      <div class="bg-white rounded-xl shadow-sm p-6 space-y-5">
        <div class="text-sm text-gray-600">
          你可以在这里提交对系统的意见、建议或问题。管理员处理后，可在“反馈记录”查看状态与回复。
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">反馈类型</label>
          <select
            v-model="category"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
          >
            <option value="suggestion">功能建议</option>
            <option value="issue">使用问题</option>
            <option value="complaint">投诉</option>
            <option value="other">其他</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">反馈内容</label>
          <textarea
            v-model="content"
            rows="6"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="请尽量描述清楚：你遇到了什么问题、期望什么改进、发生时间/场景等"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">联系方式（可选）</label>
          <input
            v-model="contact"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="手机号/邮箱/微信号（便于管理员联系）"
          />
        </div>

        <div v-if="error" class="text-sm text-red-600">{{ error }}</div>

        <div class="flex items-center justify-end gap-2">
          <button
            class="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors cursor-pointer"
            :disabled="submitting"
            @click="reset"
          >
            重置
          </button>
          <button
            class="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed"
            :disabled="submitting || !content.trim()"
            @click="submit"
          >
            {{ submitting ? '提交中...' : '提交反馈' }}
          </button>
        </div>
      </div>
    </div>

    <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
      <div v-else-if="items.length === 0" class="text-center py-12 text-gray-500">暂无反馈</div>
      <table v-else class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">时间</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">类型</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">状态</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">内容</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr
            v-for="fb in items"
            :key="fb.id"
            class="hover:bg-gray-50 cursor-pointer"
            @click="openDetail(fb)"
          >
            <td class="px-4 py-3 text-sm text-gray-600">{{ formatDateTime(fb.created_at) }}</td>
            <td class="px-4 py-3 text-sm text-gray-900">{{ fb.category_display || fb.category }}</td>
            <td class="px-4 py-3 text-sm">
              <span :class="statusBadge(fb.status)">{{ fb.status_display || fb.status }}</span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-600 line-clamp-1">{{ fb.content }}</td>
          </tr>
        </tbody>
      </table>

      <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-6 pb-6">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          上一页
        </button>
        <span class="px-4 py-2">第 {{ currentPage }} / {{ totalPages }} 页</span>
        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          下一页
        </button>
      </div>
    </div>

    <!-- 记录详情弹窗 -->
    <div v-if="selected" @click="selected = null" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div @click.stop class="bg-white rounded-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h2 class="font-heading text-xl font-bold text-textDark">反馈详情</h2>
          <button @click="selected = null" class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div class="p-6 space-y-4">
          <div class="flex flex-wrap gap-2 items-center">
            <span class="text-sm text-gray-600">类型：</span>
            <span class="text-sm font-medium text-gray-900">{{ selected.category_display || selected.category }}</span>
            <span class="mx-2 text-gray-300">|</span>
            <span :class="statusBadge(selected.status)">{{ selected.status_display || selected.status }}</span>
            <span class="ml-auto text-sm text-gray-500">{{ formatDateTime(selected.created_at) }}</span>
          </div>

          <div>
            <h3 class="text-sm font-medium text-gray-500 mb-2">我的反馈</h3>
            <p class="text-gray-900 whitespace-pre-wrap">{{ selected.content }}</p>
          </div>

          <div v-if="selected.contact">
            <h3 class="text-sm font-medium text-gray-500 mb-2">联系方式</h3>
            <p class="text-gray-900">{{ selected.contact }}</p>
          </div>

          <div class="bg-gray-50 rounded-lg p-4">
            <h3 class="text-sm font-medium text-gray-700 mb-2">管理员回复</h3>
            <p v-if="selected.admin_reply" class="text-gray-800 whitespace-pre-wrap">{{ selected.admin_reply }}</p>
            <p v-else class="text-gray-500 text-sm">暂无回复</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createFeedback, getMyFeedbacks, markAllNotificationsRead, getUnreadNotificationCount } from '@/api'
import { useNotification } from '@/composables/useNotification'

const route = useRoute()
const router = useRouter()
const { notify } = useNotification()

const activeTab = ref('submit')
const category = ref('other')
const content = ref('')
const contact = ref('')
const submitting = ref(false)
const error = ref('')
const unreadCount = ref(0)

const loading = ref(false)
const items = ref([])
const selected = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 10

onMounted(() => {
  const tab = route.query.tab === 'records' ? 'records' : 'submit'
  switchTab(tab)
  refreshUnread()
})

function reset() {
  if (submitting.value) return
  category.value = 'other'
  content.value = ''
  contact.value = ''
  error.value = ''
}

async function submit() {
  error.value = ''
  submitting.value = true
  try {
    await createFeedback({
      category: category.value,
      content: content.value,
      contact: contact.value || null,
    })
    notify({ message: '反馈已提交', type: 'success' })
    reset()
    await switchTab('records')
  } catch (e) {
    const data = e?.response?.data
    if (typeof data === 'object' && data) {
      const k = Object.keys(data)[0]
      const v = Array.isArray(data[k]) ? data[k][0] : data[k]
      error.value = v || '提交失败'
    } else {
      error.value = e?.response?.data?.error || e?.response?.data?.detail || '提交失败'
    }
  } finally {
    submitting.value = false
  }
}

async function refreshUnread() {
  try {
    const { data } = await getUnreadNotificationCount()
    unreadCount.value = data?.count ?? 0
  } catch {
    unreadCount.value = 0
  }
}

async function switchTab(tab) {
  activeTab.value = tab
  router.replace({ path: '/feedback', query: tab === 'records' ? { tab: 'records' } : {} })
  if (tab === 'records') {
    await markAllNotificationsRead().catch(() => {})
    unreadCount.value = 0
    await loadRecords()
  }
}

async function loadRecords() {
  loading.value = true
  try {
    const res = await getMyFeedbacks({ page: currentPage.value, page_size: pageSize })
    items.value = res.data.results || res.data
    if (res.data.count) totalPages.value = Math.ceil(res.data.count / pageSize)
    else totalPages.value = 1
  } catch (e) {
    notify({ message: '加载反馈失败', type: 'error' })
    items.value = []
    totalPages.value = 1
  } finally {
    loading.value = false
  }
}

function goToPage(p) {
  if (p < 1 || p > totalPages.value) return
  currentPage.value = p
  loadRecords()
}

function openDetail(fb) {
  selected.value = fb
}

function statusBadge(status) {
  const m = {
    new: 'px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs',
    in_progress: 'px-2 py-1 bg-amber-100 text-amber-700 rounded text-xs',
    resolved: 'px-2 py-1 bg-green-100 text-green-700 rounded text-xs',
    closed: 'px-2 py-1 bg-gray-200 text-gray-700 rounded text-xs',
  }
  return m[status] || 'px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs'
}

function formatDateTime(dateString) {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}
</script>

