<template>
  <div class="space-y-6 p-4 md:p-6">
    <h1 class="font-heading text-2xl font-bold text-[#1E293B]">管理仪表盘</h1>
    
    <!-- Loading Skeleton -->
    <template v-if="loading">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <div class="animate-pulse space-y-3">
            <div class="h-3 bg-gray-200 rounded w-2/3"></div>
            <div class="h-8 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div v-for="i in 4" :key="i" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <SkeletonChart />
        </div>
      </div>
    </template>
    
    <template v-else>
      <!-- KPI Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200 cursor-pointer">
          <div class="text-gray-500 text-sm font-medium">总工单</div>
          <div class="font-heading text-3xl font-bold text-primary mt-2">{{ stats.total ?? 0 }}</div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200 cursor-pointer">
          <div class="text-gray-500 text-sm font-medium">待处理</div>
          <div class="font-heading text-3xl font-bold text-[#F97316] mt-2">{{ stats.pending ?? 0 }}</div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200 cursor-pointer">
          <div class="text-gray-500 text-sm font-medium">已完成</div>
          <div class="font-heading text-3xl font-bold text-green-600 mt-2">{{ stats.completed ?? 0 }}</div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200 cursor-pointer">
          <div class="text-gray-500 text-sm font-medium">平均响应(h)</div>
          <div class="font-heading text-3xl font-bold text-[#60A5FA] mt-2">{{ stats.avg_response_time ?? '-' }}</div>
        </div>
      </div>

      <!-- Charts Row 1 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Trend Chart -->
        <div class="bg-white rounded-xl p-4 md:p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
          <h2 class="font-heading text-base md:text-lg font-semibold text-[#1E293B] mb-4">工单趋势（最近7天）</h2>
          <div class="h-56 md:h-64">
            <LineChart v-if="trendData" :data="trendData" />
            <div v-else class="flex items-center justify-center h-full text-gray-400 text-sm">暂无数据</div>
          </div>
        </div>

        <!-- Type Distribution -->
        <div class="bg-white rounded-xl p-4 md:p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
          <h2 class="font-heading text-base md:text-lg font-semibold text-[#1E293B] mb-4">故障类型分布</h2>
          <div class="h-56 md:h-64">
            <DoughnutChart v-if="typeDistData" :data="typeDistData" />
            <div v-else class="flex items-center justify-center h-full text-gray-400 text-sm">暂无数据</div>
          </div>
        </div>
      </div>

      <!-- Charts Row 2 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Repairman Performance -->
        <div class="bg-white rounded-xl p-4 md:p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
          <h2 class="font-heading text-base md:text-lg font-semibold text-[#1E293B] mb-4">维修员绩效对比</h2>
          <div class="h-56 md:h-64">
            <RadarChart v-if="performanceData" :data="performanceData" />
            <div v-else class="flex items-center justify-center h-full text-gray-400 text-sm">暂无数据</div>
          </div>
        </div>

        <!-- Pending Orders List -->
        <div class="bg-white rounded-xl p-4 md:p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
          <h2 class="font-heading text-base md:text-lg font-semibold text-[#1E293B] mb-4">待处理工单</h2>
          <div v-if="pendingList.length === 0" class="text-gray-400 py-8 text-center text-sm">暂无待处理工单</div>
          <ul v-else class="divide-y divide-gray-100 max-h-56 overflow-y-auto">
            <li v-for="o in pendingList" :key="o.id" class="py-3 flex justify-between items-center hover:bg-gray-50 px-2 rounded transition-colors duration-150 cursor-pointer">
              <span class="text-sm text-[#475569]">{{ o.order_sn }} - {{ o.content?.slice(0, 25) }}...</span>
              <router-link :to="'/orders'" class="text-[#3B82F6] text-sm font-medium hover:text-[#60A5FA] transition-colors duration-150">查看</router-link>
            </li>
          </ul>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getStatistics, getPendingOrders, getTrendData, getTypeDistribution, getRepairmanPerformance } from '@/api'
import { useUserStore } from '@/stores/user'
import LineChart from '@/components/charts/LineChart.vue'
import DoughnutChart from '@/components/charts/DoughnutChart.vue'
import RadarChart from '@/components/charts/RadarChart.vue'
import SkeletonChart from '@/components/SkeletonChart.vue'

const userStore = useUserStore()
const loading = ref(true)
const stats = ref({})
const pendingList = ref([])
const trendRaw = ref([])
const typeDistRaw = ref([])
const performanceRaw = ref([])

const trendData = computed(() => {
  if (!trendRaw.value.length) return null
  return {
    labels: trendRaw.value.map(d => d.date),
    datasets: [
      {
        label: '提交工单',
        data: trendRaw.value.map(d => d.submitted),
        borderColor: '#3B82F6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)'
      },
      {
        label: '完成工单',
        data: trendRaw.value.map(d => d.completed),
        borderColor: '#10B981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)'
      }
    ]
  }
})

const typeDistData = computed(() => {
  if (!typeDistRaw.value.length) return null
  return {
    labels: typeDistRaw.value.map(d => d.category || '未分类'),
    values: typeDistRaw.value.map(d => d.count)
  }
})

const performanceData = computed(() => {
  if (!performanceRaw.value.length) return null
  
  // 调试：打印原始数据
  console.log('Performance Raw Data:', performanceRaw.value)
  
  const labels = ['响应速度', '维修质量', '工单数量', '用户评分', '准时率']
  return {
    labels,
    datasets: performanceRaw.value.map(p => {
      const data = [
        p.response_speed || 50,
        p.quality || 50,
        p.quantity || 50,
        p.rating || 50,
        p.punctuality || 50
      ]
      console.log(`${p.name} 数据:`, data)
      return {
        label: p.name,
        data
      }
    })
  }
})

onMounted(async () => {
  if (userStore.user?.role !== 3) {
    loading.value = false
    return
  }
  
  try {
    const [statsRes, pendingRes, trendRes, typeRes, perfRes] = await Promise.all([
      getStatistics(),
      getPendingOrders(),
      getTrendData(),
      getTypeDistribution(),
      getRepairmanPerformance()
    ])
    
    stats.value = statsRes.data || {}
    pendingList.value = Array.isArray(pendingRes.data) ? pendingRes.data : pendingRes.data?.results ?? []
    trendRaw.value = trendRes.data || []
    typeDistRaw.value = typeRes.data || []
    performanceRaw.value = perfRes.data || []
  } catch (err) {
    console.error('加载仪表盘数据失败:', err)
    stats.value = {}
    pendingList.value = []
  } finally {
    loading.value = false
  }
})
</script>
