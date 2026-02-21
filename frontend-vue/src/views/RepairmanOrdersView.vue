<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">我的工单</h1>
    
    <!-- 状态筛选 -->
    <div class="flex gap-2 mb-6 flex-wrap">
      <button v-for="s in statusFilters" :key="s.value"
        :class="['px-4 py-2 rounded-lg transition-colors cursor-pointer', 
          filterStatus === s.value ? 'bg-primary text-white' : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50']"
        @click="filterStatus = s.value">
        {{ s.label }}
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
    
    <!-- 空状态 -->
    <div v-else-if="!filteredList.length" 
      class="bg-white rounded-xl p-8 text-center text-gray-500">
      暂无工单
    </div>
    
    <!-- 工单列表 -->
    <div v-else class="space-y-4">
      <div v-for="order in filteredList" :key="order.id" 
        class="bg-white rounded-xl shadow-sm p-4 border border-gray-100 hover:shadow-md transition-shadow">
        <div class="flex gap-4">
          <!-- 图片缩略图 -->
          <div v-if="order.img_proof" class="flex-shrink-0">
            <img :src="order.img_proof" :alt="order.repair_type_info?.name" 
              class="w-20 h-20 object-cover rounded-lg border border-gray-200 cursor-pointer"
              @click="showOrderDetail(order)">
          </div>
          
          <!-- 工单信息 -->
          <div class="flex-1 min-w-0">
            <div class="flex justify-between items-start gap-2">
              <div>
                <span class="font-heading font-medium text-textDark cursor-pointer hover:text-primary"
                  @click="showOrderDetail(order)">
                  {{ order.order_sn }}
                </span>
                <span :class="statusClass(order.status)" class="ml-2">
                  {{ order.status_display }}
                </span>
              </div>
            </div>
            <p class="text-gray-600 mt-2 text-sm">
              {{ order.repair_type_info?.name }} · {{ order.priority_display }}
            </p>
            <p class="text-gray-700 mt-1 line-clamp-2">{{ order.content }}</p>
            <p class="text-gray-400 text-xs mt-2">{{ order.create_time }}</p>
          </div>
          
          <!-- 操作按钮 -->
          <div class="flex-shrink-0 flex flex-col gap-2">
            <button v-if="order.status === 1" 
              @click="handleStartRepair(order)"
              :disabled="operating === order.id"
              class="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors cursor-pointer text-sm disabled:opacity-50">
              <span v-if="operating === order.id">处理中...</span>
              <span v-else>开始维修</span>
            </button>
            
            <button v-if="order.status === 2" 
              @click="showCompleteDialog(order)"
              class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors cursor-pointer text-sm">
              完成维修
            </button>
            
            <button @click="showOrderDetail(order)"
              class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer text-sm">
              查看详情
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 工单详情弹窗 -->
    <div v-if="selectedOrder && showDetail" @click="showDetail = false" 
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div @click.stop class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h2 class="font-heading text-xl font-bold text-textDark">工单详情</h2>
          <button @click="showDetail = false" class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer">
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
            <div v-if="selectedOrder.accept_time" class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">接单时间：</span>
              <span class="text-gray-900">{{ selectedOrder.accept_time }}</span>
            </div>
            <div v-if="selectedOrder.start_time" class="flex items-center gap-2 text-sm">
              <span class="text-gray-500">开始维修：</span>
              <span class="text-gray-900">{{ selectedOrder.start_time }}</span>
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

          <!-- 维修凭证 -->
          <div v-if="selectedOrder.status === 3 && (selectedOrder.repair_proof_img || selectedOrder.repair_description)">
            <h3 class="text-sm font-medium text-gray-500 mb-2">维修凭证</h3>
            <div class="bg-green-50 rounded-lg p-4 space-y-3">
              <img v-if="selectedOrder.repair_proof_img" :src="selectedOrder.repair_proof_img" 
                class="w-full h-auto rounded-lg border border-green-200">
              <p v-if="selectedOrder.repair_description" class="text-gray-900 whitespace-pre-wrap">
                {{ selectedOrder.repair_description }}
              </p>
            </div>
          </div>

          <!-- 备注 -->
          <div v-if="selectedOrder.remark">
            <h3 class="text-sm font-medium text-gray-500 mb-2">备注</h3>
            <p class="text-gray-900 whitespace-pre-wrap">{{ selectedOrder.remark }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 完成维修对话框 -->
    <CompleteRepairDialog
      v-if="showComplete"
      :order="selectedOrder"
      @close="showComplete = false"
      @submit="handleCompleteSubmit"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMyOrders, startRepair } from '@/api'
import CompleteRepairDialog from '@/components/CompleteRepairDialog.vue'
import { useNotification } from '@/composables/useNotification'

const { notify, confirm } = useNotification()
const loading = ref(true)
const list = ref([])
const filterStatus = ref('')
const selectedOrder = ref(null)
const showDetail = ref(false)
const showComplete = ref(false)
const operating = ref(null)

const statusFilters = [
  { value: '', label: '全部' },
  { value: '1', label: '已派单' },
  { value: '2', label: '维修中' },
  { value: '3', label: '已完成' },
]

const statusClass = (status) => {
  const m = { 
    0: 'text-amber-600', 
    1: 'text-blue-600', 
    2: 'text-orange-600', 
    3: 'text-green-600', 
    4: 'text-gray-500' 
  }
  return m[status] || 'text-gray-600'
}

const filteredList = computed(() => {
  if (filterStatus.value === '') return list.value
  return list.value.filter((o) => String(o.status) === filterStatus.value)
})

const showOrderDetail = (order) => {
  selectedOrder.value = order
  showDetail.value = true
}

const showCompleteDialog = (order) => {
  selectedOrder.value = order
  showComplete.value = true
}

const handleStartRepair = async (order) => {
  const confirmed = await confirm({
    title: '确认开始维修',
    message: `确定要开始维修工单 ${order.order_sn} 吗？`,
    confirmText: '开始维修',
    cancelText: '取消',
    type: 'info'
  })
  
  if (!confirmed) return
  
  operating.value = order.id
  
  try {
    await startRepair(order.id)
    notify({
      message: '已开始维修',
      type: 'success'
    })
    await load()
  } catch (error) {
    console.error('操作失败:', error)
    notify({
      message: error.response?.data?.error || '操作失败，请重试',
      type: 'error'
    })
  } finally {
    operating.value = null
  }
}

const handleCompleteSubmit = async () => {
  await load()
}

async function load() {
  loading.value = true
  try {
    const { data } = await getMyOrders()
    list.value = Array.isArray(data) ? data : data?.results ?? []
  } catch (error) {
    console.error('加载工单失败:', error)
    list.value = []
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
