<template>
  <div>
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">我的工单</h1>
    <div class="flex gap-2 mb-4 flex-wrap">
      <button v-for="s in statusFilters" :key="s.value"
        :class="['px-4 py-2 rounded-lg transition-colors cursor-pointer', filterStatus === s.value ? 'bg-primary text-white' : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50']"
        @click="filterStatus = s.value">
        {{ s.label }}
      </button>
    </div>
    <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
    <div v-else-if="!filteredList.length" class="bg-white rounded-xl p-8 text-center text-gray-500">暂无工单</div>
    <div v-else class="space-y-4">
      <div v-for="order in filteredList" :key="order.id" 
        @click="selectedOrder = order"
        class="bg-white rounded-xl shadow-sm p-4 border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
        <div class="flex gap-4">
          <!-- 图片缩略图 -->
          <div v-if="order.img_proof" class="flex-shrink-0">
            <img :src="order.img_proof" :alt="order.repair_type_info?.name" 
              class="w-20 h-20 object-cover rounded-lg border border-gray-200">
          </div>
          
          <!-- 工单信息 -->
          <div class="flex-1 min-w-0">
            <div class="flex justify-between items-start gap-2">
              <span class="font-heading font-medium text-textDark">{{ order.order_sn }}</span>
              <span :class="statusClass(order.status)" class="flex-shrink-0">{{ order.status_display }}</span>
            </div>
            <p class="text-gray-600 mt-2 text-sm">{{ order.repair_type_info?.name }} · {{ order.priority_display }}</p>
            <p class="text-gray-700 mt-1 line-clamp-2">{{ order.content }}</p>
            <p class="text-gray-400 text-xs mt-2">{{ order.create_time }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 工单详情弹窗 -->
    <div v-if="selectedOrder" @click="selectedOrder = null" 
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div @click.stop class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h2 class="font-heading text-xl font-bold text-textDark">工单详情</h2>
          <button @click="selectedOrder = null" class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="p-6 space-y-4">
          <!-- 工单编号和状态 -->
          <div class="flex justify-between items-center">
            <span class="font-medium text-gray-900">{{ selectedOrder.order_sn }}</span>
            <span :class="statusClass(selectedOrder.status)" class="px-3 py-1 rounded-full text-sm">
              {{ selectedOrder.status_display }}
            </span>
          </div>

          <!-- 图片 -->
          <div v-if="selectedOrder.img_proof" class="rounded-lg overflow-hidden border border-gray-200">
            <img :src="selectedOrder.img_proof" :alt="selectedOrder.repair_type_info?.name" 
              class="w-full h-auto">
          </div>

          <!-- 基本信息 -->
          <div class="space-y-2">
            <div class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">故障类型：</span>
              <span class="text-gray-900">{{ selectedOrder.repair_type_info?.name }}</span>
            </div>
            <div class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">紧急程度：</span>
              <span class="text-gray-900">{{ selectedOrder.priority_display }}</span>
            </div>
            <div class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">提交时间：</span>
              <span class="text-gray-900">{{ selectedOrder.create_time }}</span>
            </div>
            <div v-if="selectedOrder.repairman_info" class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">维修员：</span>
              <span class="text-gray-900">{{ selectedOrder.repairman_info.username }}</span>
            </div>
            <div v-if="selectedOrder.finish_time" class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">完成时间：</span>
              <span class="text-gray-900">{{ selectedOrder.finish_time }}</span>
            </div>
          </div>

          <!-- 问题描述 -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 mb-2">问题描述</h3>
            <p class="text-gray-900 whitespace-pre-wrap">{{ selectedOrder.content }}</p>
          </div>

          <!-- 备注 -->
          <div v-if="selectedOrder.remark">
            <h3 class="text-sm font-medium text-gray-500 mb-2">备注</h3>
            <p class="text-gray-900 whitespace-pre-wrap">{{ selectedOrder.remark }}</p>
          </div>

          <!-- 评价 -->
          <div v-if="selectedOrder.comment" class="bg-amber-50 rounded-lg p-4">
            <h3 class="text-sm font-medium text-gray-700 mb-2">我的评价</h3>
            <div class="flex items-center gap-1 mb-2">
              <svg v-for="i in 5" :key="i" class="w-5 h-5" 
                :class="i <= selectedOrder.comment.score ? 'text-amber-400' : 'text-gray-300'"
                fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
              </svg>
            </div>
            <p v-if="selectedOrder.comment.feedback" class="text-gray-700 text-sm">
              {{ selectedOrder.comment.feedback }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMyOrders } from '@/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const loading = ref(true)
const list = ref([])
const filterStatus = ref('')
const selectedOrder = ref(null)

const statusFilters = [
  { value: '', label: '全部' },
  { value: '0', label: '待审核' },
  { value: '1', label: '已派单' },
  { value: '2', label: '维修中' },
  { value: '3', label: '已完成' },
  { value: '4', label: '已取消' },
]

const statusClass = (status) => {
  const m = { 0: 'text-amber-600', 1: 'text-blue-600', 2: 'text-primary', 3: 'text-green-600', 4: 'text-gray-500' }
  return m[status] || 'text-gray-600'
}

const filteredList = computed(() => {
  if (filterStatus.value === '') return list.value
  return list.value.filter((o) => String(o.status) === filterStatus.value)
})

async function load() {
  if (!userStore.user) return
  loading.value = true
  try {
    const { data } = await getMyOrders()
    list.value = Array.isArray(data) ? data : data?.results ?? []
  } catch {
    list.value = []
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
