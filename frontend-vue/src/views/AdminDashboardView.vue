<template>
  <div>
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">管理仪表盘</h1>
    <div v-if="!stats" class="text-center py-12 text-gray-500">加载中...</div>
    <template v-else>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <div class="text-gray-500 text-sm">待处理</div>
          <div class="font-heading text-2xl font-bold text-primary mt-1">{{ stats.pending ?? 0 }}</div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <div class="text-gray-500 text-sm">维修中</div>
          <div class="font-heading text-2xl font-bold text-primary mt-1">{{ stats.in_progress ?? 0 }}</div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <div class="text-gray-500 text-sm">本月完成</div>
          <div class="font-heading text-2xl font-bold text-green-600 mt-1">{{ stats.completed ?? 0 }}</div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <div class="text-gray-500 text-sm">平均响应(h)</div>
          <div class="font-heading text-2xl font-bold text-cta mt-1">{{ stats.avg_response_time ?? '-' }}</div>
        </div>
      </div>
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <h2 class="font-heading text-lg font-semibold text-textDark mb-4">待处理工单</h2>
        <div v-if="pendingList.length === 0" class="text-gray-500 py-8 text-center">暂无待处理工单</div>
        <ul v-else class="divide-y divide-gray-100">
          <li v-for="o in pendingList" :key="o.id" class="py-3 flex justify-between items-center">
            <span>{{ o.order_sn }} - {{ o.content?.slice(0, 30) }}...</span>
            <router-link :to="'/orders'" class="text-primary text-sm font-medium">查看</router-link>
          </li>
        </ul>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getStatistics, getPendingOrders } from '@/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const stats = ref(null)
const pendingList = ref([])

onMounted(async () => {
  if (userStore.user?.role !== 3) return
  try {
    const [s, p] = await Promise.all([getStatistics(), getPendingOrders()])
    stats.value = s.data
    pendingList.value = Array.isArray(p.data) ? p.data : p.data?.results ?? []
  } catch {
    stats.value = {}
    pendingList.value = []
  }
})
</script>
