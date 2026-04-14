<template>
  <div>
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">反馈管理</h1>

    <!-- 筛选 -->
    <div class="bg-white rounded-xl p-4 shadow-sm mb-4">
      <div class="flex flex-wrap gap-4">
        <input
          v-model="filters.search"
          @input="handleFilter"
          type="text"
          placeholder="搜索内容/回复/用户名..."
          class="flex-1 min-w-[200px] px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <select
          v-model="filters.status"
          @change="handleFilter"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
        >
          <option value="">全部状态</option>
          <option value="new">新提交</option>
          <option value="in_progress">处理中</option>
          <option value="resolved">已解决</option>
          <option value="closed">已关闭</option>
        </select>
        <select
          v-model="filters.category"
          @change="handleFilter"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
        >
          <option value="">全部类型</option>
          <option value="suggestion">功能建议</option>
          <option value="issue">使用问题</option>
          <option value="complaint">投诉</option>
          <option value="other">其他</option>
        </select>
      </div>
    </div>

    <!-- 列表 -->
    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
      <div v-else-if="items.length === 0" class="text-center py-12 text-gray-500">暂无反馈</div>
      <table v-else class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">时间</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">用户</th>
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
            <td class="px-4 py-3 text-sm text-gray-900">
              {{ fb.user_info?.real_name || fb.user_info?.username || fb.user }}
            </td>
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

    <!-- 处理弹窗 -->
    <div v-if="selected" @click="closeDetail" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div @click.stop class="bg-white rounded-xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
        <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h2 class="font-heading text-xl font-bold text-textDark">处理反馈</h2>
          <button @click="closeDetail" class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div class="p-6 space-y-5">
          <div class="flex flex-wrap gap-2 items-center">
            <span class="text-sm text-gray-600">用户：</span>
            <span class="text-sm font-medium text-gray-900">{{ selected.user_info?.real_name || selected.user_info?.username }}</span>
            <span class="mx-2 text-gray-300">|</span>
            <span class="text-sm text-gray-600">类型：</span>
            <span class="text-sm font-medium text-gray-900">{{ selected.category_display || selected.category }}</span>
            <span class="ml-auto text-sm text-gray-500">{{ formatDateTime(selected.created_at) }}</span>
          </div>

          <div>
            <h3 class="text-sm font-medium text-gray-500 mb-2">反馈内容</h3>
            <p class="text-gray-900 whitespace-pre-wrap">{{ selected.content }}</p>
          </div>

          <div v-if="selected.contact">
            <h3 class="text-sm font-medium text-gray-500 mb-2">联系方式</h3>
            <p class="text-gray-900">{{ selected.contact }}</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
              <select
                v-model="edit.status"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
              >
                <option value="new">新提交</option>
                <option value="in_progress">处理中</option>
                <option value="resolved">已解决</option>
                <option value="closed">已关闭</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">管理员回复</label>
            <textarea
              v-model="edit.admin_reply"
              rows="5"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="写下对用户可见的回复/处理结果"
            />
          </div>

          <div v-if="saveError" class="text-sm text-red-600">{{ saveError }}</div>

          <div class="flex items-center justify-end gap-2">
            <button
              class="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors cursor-pointer"
              :disabled="saving"
              @click="closeDetail"
            >
              取消
            </button>
            <button
              class="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed"
              :disabled="saving"
              @click="save"
            >
              {{ saving ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFeedbacks, handleFeedback } from '@/api'
import { useNotification } from '@/composables/useNotification'

const { notify } = useNotification()
const loading = ref(false)
const items = ref([])

const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 10

const filters = ref({
  search: '',
  status: '',
  category: '',
})

const selected = ref(null)
const edit = ref({ status: 'new', admin_reply: '' })
const saving = ref(false)
const saveError = ref('')

onMounted(() => load())

async function load() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize,
    }
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.category) params.category = filters.value.category

    const res = await getFeedbacks(params)
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

function handleFilter() {
  currentPage.value = 1
  load()
}

function goToPage(p) {
  if (p < 1 || p > totalPages.value) return
  currentPage.value = p
  load()
}

function openDetail(fb) {
  selected.value = fb
  edit.value = {
    status: fb.status || 'new',
    admin_reply: fb.admin_reply || '',
  }
  saveError.value = ''
}

function closeDetail() {
  if (saving.value) return
  selected.value = null
}

async function save() {
  if (!selected.value) return
  saveError.value = ''
  saving.value = true
  try {
    const updated = await handleFeedback(selected.value.id, {
      status: edit.value.status,
      admin_reply: edit.value.admin_reply || null,
    })
    // 更新本地列表
    const idx = items.value.findIndex((x) => x.id === selected.value.id)
    const next = updated.data
    if (idx >= 0) items.value[idx] = next
    selected.value = next
    notify({ message: '已保存', type: 'success' })
    await load()
    closeDetail()
  } catch (e) {
    const data = e?.response?.data
    if (typeof data === 'object' && data) {
      const k = Object.keys(data)[0]
      const v = Array.isArray(data[k]) ? data[k][0] : data[k]
      saveError.value = v || '保存失败'
    } else {
      saveError.value = e?.response?.data?.error || e?.response?.data?.detail || '保存失败'
    }
  } finally {
    saving.value = false
  }
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

