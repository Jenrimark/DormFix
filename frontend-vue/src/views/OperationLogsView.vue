<template>
  <div>
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">用户日志</h1>

    <!-- 筛选条件 -->
    <div class="bg-white rounded-xl p-4 shadow-sm mb-4">
      <div class="flex flex-wrap gap-4">
        <input
          v-model="filters.operator"
          @input="handleFilter"
          type="text"
          placeholder="操作人..."
          class="flex-1 min-w-[150px] px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <select
          v-model="filters.action"
          @change="handleFilter"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
        >
          <option value="">全部操作</option>
          <option value="create">创建</option>
          <option value="update">更新</option>
          <option value="delete">删除</option>
          <option value="enable">启用</option>
          <option value="disable">禁用</option>
          <option value="reset_password">重置密码</option>
          <option value="batch_enable">批量启用</option>
          <option value="batch_disable">批量禁用</option>
          <option value="batch_delete">批量删除</option>
        </select>
        <input
          v-model="filters.start_date"
          @change="handleFilter"
          type="date"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <input
          v-model="filters.end_date"
          @change="handleFilter"
          type="date"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>
    </div>

    <!-- 日志列表 -->
    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
      <div v-else-if="logs.length === 0" class="text-center py-12 text-gray-500">暂无日志记录</div>
      <table v-else class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">时间</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">操作人</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">操作类型</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">描述</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">IP地址</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="log in logs" :key="log.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 text-sm text-gray-600">{{ formatDateTime(log.created_at) }}</td>
            <td class="px-4 py-3 text-sm text-gray-900">{{ log.operator_real_name || log.operator_username || log.operator || '-' }}</td>
            <td class="px-4 py-3 text-sm">
              <span :class="getActionBadgeClass(log.action)">
                {{ log.action_display || getActionText(log.action) }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-600">{{ log.description || '-' }}</td>
            <td class="px-4 py-3 text-sm text-gray-600">{{ log.ip_address || '-' }}</td>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getOperationLogs } from '@/api'

const logs = ref([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 20
const filters = ref({
  operator: '',
  action: '',
  start_date: '',
  end_date: ''
})

onMounted(() => {
  loadLogs()
})

async function loadLogs() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize
    }
    if (filters.value.operator) params.operator = filters.value.operator
    if (filters.value.action) params.action = filters.value.action
    if (filters.value.start_date) params.start_date = filters.value.start_date
    if (filters.value.end_date) params.end_date = filters.value.end_date

    const res = await getOperationLogs(params)
    logs.value = res.data.results || res.data
    if (res.data.count) {
      totalPages.value = Math.ceil(res.data.count / pageSize)
    }
  } catch (error) {
    console.error('加载用户日志失败:', error)
    alert('加载用户日志失败')
  } finally {
    loading.value = false
  }
}

function handleFilter() {
  currentPage.value = 1
  loadLogs()
}

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    loadLogs()
  }
}

function getActionText(action) {
  const actionMap = {
    create: '创建',
    update: '更新',
    delete: '删除',
    enable: '启用',
    disable: '禁用',
    reset_password: '重置密码',
    batch_enable: '批量启用',
    batch_disable: '批量禁用',
    batch_delete: '批量删除'
  }
  return actionMap[action] || action
}

function getActionBadgeClass(action) {
  const classMap = {
    create: 'px-2 py-1 bg-green-100 text-green-700 rounded text-xs',
    update: 'px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs',
    delete: 'px-2 py-1 bg-red-100 text-red-700 rounded text-xs',
    enable: 'px-2 py-1 bg-green-100 text-green-700 rounded text-xs',
    disable: 'px-2 py-1 bg-yellow-100 text-yellow-700 rounded text-xs',
    reset_password: 'px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs',
    batch_enable: 'px-2 py-1 bg-green-100 text-green-700 rounded text-xs',
    batch_disable: 'px-2 py-1 bg-yellow-100 text-yellow-700 rounded text-xs',
    batch_delete: 'px-2 py-1 bg-red-100 text-red-700 rounded text-xs'
  }
  return classMap[action] || 'px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs'
}

function formatDateTime(dateString) {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>
