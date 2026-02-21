<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">工单审核</h1>
    
    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="bg-white rounded-xl shadow-sm p-4 border border-gray-100">
        <div class="text-gray-500 text-sm mb-1">待审核</div>
        <div class="text-2xl font-bold text-amber-600">{{ pendingCount }}</div>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-4 border border-gray-100">
        <div class="text-gray-500 text-sm mb-1">今日已审核</div>
        <div class="text-2xl font-bold text-green-600">{{ todayReviewed }}</div>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-4 border border-gray-100">
        <div class="text-gray-500 text-sm mb-1">审核通过率</div>
        <div class="text-2xl font-bold text-blue-600">{{ passRate }}%</div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
    
    <!-- 空状态 -->
    <div v-else-if="!pendingOrders.length" 
      class="bg-white rounded-xl p-8 text-center text-gray-500">
      <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
      </svg>
      <p>暂无待审核工单</p>
    </div>
    
    <!-- 工单列表 -->
    <div v-else class="space-y-4">
      <div v-for="order in pendingOrders" :key="order.id" 
        @click="showReviewDialog(order)"
        class="bg-white rounded-xl shadow-sm p-4 border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
        <div class="flex gap-4">
          <!-- 图片缩略图 -->
          <div v-if="order.img_proof" class="flex-shrink-0">
            <img :src="order.img_proof" :alt="order.repair_type_info?.name" 
              class="w-24 h-24 object-cover rounded-lg border border-gray-200">
          </div>
          <div v-else class="flex-shrink-0 w-24 h-24 bg-gray-100 rounded-lg flex items-center justify-center">
            <svg class="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </div>
          
          <!-- 工单信息 -->
          <div class="flex-1 min-w-0">
            <div class="flex justify-between items-start gap-2 mb-2">
              <div>
                <span class="font-heading font-medium text-textDark">{{ order.order_sn }}</span>
                <span :class="priorityBadgeClass(order.priority)" class="ml-2 px-2 py-0.5 rounded text-xs">
                  {{ order.priority_display }}
                </span>
              </div>
              <span class="text-amber-600 text-sm flex-shrink-0">待审核</span>
            </div>
            
            <div class="space-y-1 text-sm">
              <p class="text-gray-600">
                <span class="font-medium">{{ order.repair_type_info?.name }}</span>
                <span class="mx-2">·</span>
                <span>{{ order.user_info?.real_name || order.user_info?.username }}</span>
              </p>
              <p class="text-gray-700 line-clamp-2">{{ order.content }}</p>
              <p class="text-gray-400 text-xs">{{ formatTime(order.create_time) }}</p>
            </div>
          </div>
          
          <!-- 操作按钮 -->
          <div class="flex-shrink-0 flex items-center">
            <button @click.stop="showReviewDialog(order)" 
              class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors cursor-pointer">
              审核
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 审核对话框 -->
    <ReviewDialog
      v-if="showDialog"
      :order="selectedOrder"
      @close="showDialog = false"
      @submit="handleReviewSubmit"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getPendingOrders } from '@/api'
import ReviewDialog from '@/components/ReviewDialog.vue'

const loading = ref(true)
const pendingOrders = ref([])
const selectedOrder = ref(null)
const showDialog = ref(false)

const pendingCount = computed(() => pendingOrders.value.length)
const todayReviewed = ref(0)
const passRate = ref(95)

const priorityBadgeClass = (priority) => {
  const classes = {
    'high': 'bg-red-100 text-red-700',
    'medium': 'bg-orange-100 text-orange-700',
    'low': 'bg-gray-100 text-gray-700'
  }
  return classes[priority] || 'bg-gray-100 text-gray-700'
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN')
}

const showReviewDialog = (order) => {
  selectedOrder.value = order
  showDialog.value = true
}

const handleReviewSubmit = async () => {
  // 重新加载待审核工单列表
  await loadPendingOrders()
}

const loadPendingOrders = async () => {
  loading.value = true
  try {
    const { data } = await getPendingOrders()
    pendingOrders.value = Array.isArray(data) ? data : data?.results ?? []
  } catch (error) {
    console.error('加载待审核工单失败:', error)
    pendingOrders.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPendingOrders()
})
</script>
