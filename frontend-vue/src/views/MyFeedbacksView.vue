<template>
  <div>
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">我的反馈</h1>

    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
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
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-6">
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

    <!-- 详情弹窗 -->
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
import { getMyFeedbacks, markAllNotificationsRead } from '@/api'
import { useNotification } from '@/composables/useNotification'

const { notify } = useNotification()
const loading = ref(false)
const items = ref([])
const selected = ref(null)

const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 10

onMounted(() => {
  load()
  // 用户进入“我的反馈”默认认为已查看回复，清空红点
  markAllNotificationsRead().catch(() => {})
})

async function load() {
  loading.value = true
  try {
    const res = await getMyFeedbacks({ page: currentPage.value, page_size: pageSize })
    items.value = res.data.results || res.data
    if (res.data.count) totalPages.value = Math.ceil(res.data.count / pageSize)
  } catch (e) {
    console.error('加载反馈失败:', e)
    notify({ message: '加载反馈失败', type: 'error' })
    items.value = []
  } finally {
    loading.value = false
  }
}

function goToPage(p) {
  if (p < 1 || p > totalPages.value) return
  currentPage.value = p
  load()
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

