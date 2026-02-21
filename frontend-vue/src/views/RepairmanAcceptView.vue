<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">接单池</h1>
    
    <!-- 提示信息 -->
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
      <div class="flex items-start gap-3">
        <svg class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
        </svg>
        <div class="flex-1">
          <p class="text-sm text-blue-800">
            这里显示所有已审核通过、等待接单的工单。紧急工单会优先显示。
          </p>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
    
    <!-- 空状态 -->
    <div v-else-if="!availableOrders.length" 
      class="bg-white rounded-xl p-8 text-center text-gray-500">
      <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
          d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
      </svg>
      <p>暂无可接单工单</p>
    </div>
    
    <!-- 工单列表 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="order in availableOrders" :key="order.id" 
        class="bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-lg transition-all cursor-pointer overflow-hidden">
        <!-- 图片 -->
        <div v-if="order.img_proof" class="relative h-48 overflow-hidden">
          <img :src="order.img_proof" :alt="order.repair_type_info?.name" 
            class="w-full h-full object-cover">
          <div :class="priorityBadgeClass(order.priority)" 
            class="absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-medium">
            {{ order.priority_display }}
          </div>
        </div>
        <div v-else class="relative h-48 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
          <svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
          <div :class="priorityBadgeClass(order.priority)" 
            class="absolute top-3 right-3 px-3 py-1 rounded-full text-xs font-medium">
            {{ order.priority_display }}
          </div>
        </div>
        
        <!-- 工单信息 -->
        <div class="p-4">
          <div class="mb-2">
            <h3 class="font-heading font-medium text-textDark text-lg mb-1">
              {{ order.repair_type_info?.name }}
            </h3>
            <p class="text-sm text-gray-500">{{ order.order_sn }}</p>
          </div>
          
          <p class="text-gray-700 text-sm line-clamp-2 mb-3">{{ order.content }}</p>
          
          <div class="flex items-center justify-between text-xs text-gray-500 mb-3">
            <span>{{ order.user_info?.real_name || order.user_info?.username }}</span>
            <span>{{ formatTime(order.create_time) }}</span>
          </div>
          
          <!-- 接单按钮 -->
          <button @click="handleAccept(order)" 
            :disabled="accepting === order.id"
            class="w-full px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed">
            <span v-if="accepting === order.id">接单中...</span>
            <span v-else>接单</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAvailableOrders, acceptOrder } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(true)
const availableOrders = ref([])
const accepting = ref(null)

const priorityBadgeClass = (priority) => {
  const classes = {
    'high': 'bg-red-500 text-white',
    'medium': 'bg-orange-500 text-white',
    'low': 'bg-gray-500 text-white'
  }
  return classes[priority] || 'bg-gray-500 text-white'
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

const handleAccept = async (order) => {
  if (!confirm(`确定要接取工单 ${order.order_sn} 吗？`)) {
    return
  }
  
  accepting.value = order.id
  
  try {
    await acceptOrder(order.id)
    alert('接单成功！')
    
    // 从列表中移除已接单的工单
    availableOrders.value = availableOrders.value.filter(o => o.id !== order.id)
    
    // 可选：跳转到我的工单页面
    // router.push('/repairman/orders')
  } catch (error) {
    console.error('接单失败:', error)
    alert(error.response?.data?.error || '接单失败，请重试')
  } finally {
    accepting.value = null
  }
}

const loadAvailableOrders = async () => {
  loading.value = true
  try {
    const { data } = await getAvailableOrders()
    availableOrders.value = Array.isArray(data) ? data : data?.results ?? []
  } catch (error) {
    console.error('加载接单池失败:', error)
    availableOrders.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAvailableOrders()
})
</script>
