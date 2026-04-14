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
      <div @click.stop class="bg-white rounded-xl w-full max-w-5xl h-[85vh] overflow-hidden">
        <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h2 class="font-heading text-xl font-bold text-textDark">工单详情</h2>
          <button @click="showDetail = false" class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="p-6 h-[calc(85vh-73px)] overflow-y-auto">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
            <!-- 左列：图片 + 基本信息 -->
            <div class="space-y-4">
              <!-- 工单编号和状态 -->
              <div class="flex items-center justify-between gap-3">
                <span class="font-medium text-gray-900">{{ selectedOrder.order_sn }}</span>
                <span :class="statusClass(selectedOrder.status)" class="px-3 py-1 rounded-full text-sm whitespace-nowrap">
                  {{ selectedOrder.status_display }}
                </span>
              </div>

              <!-- 图片 -->
              <div v-if="selectedOrder.img_proof" class="rounded-lg overflow-hidden border border-gray-200 bg-gray-50">
                <button
                  type="button"
                  class="block w-full cursor-zoom-in"
                  @click="openImagePreview(selectedOrder.img_proof)"
                  aria-label="点击放大查看图片"
                >
                  <img
                    :src="selectedOrder.img_proof"
                    :alt="selectedOrder.repair_type_info?.name"
                    class="w-full max-h-64 object-cover"
                  >
                </button>
                <div class="px-3 py-2 text-xs text-gray-500 border-t border-gray-200 bg-white">
                  点击图片可放大查看
                </div>
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
            </div>

            <!-- 右列：凭证/描述/备注/评价 -->
            <div class="space-y-4">
              <!-- 维修凭证 -->
              <div v-if="selectedOrder.status === 3 && (selectedOrder.repair_proof_img || selectedOrder.repair_description)">
                <h3 class="text-sm font-medium text-gray-500 mb-2">维修凭证</h3>
                <div class="bg-green-50 rounded-lg p-4 space-y-3">
                  <div v-if="selectedOrder.repair_proof_img" class="rounded-lg overflow-hidden border border-green-200 bg-white">
                    <button
                      type="button"
                      class="block w-full cursor-zoom-in"
                      @click="openImagePreview(selectedOrder.repair_proof_img)"
                      aria-label="点击放大查看维修凭证图片"
                    >
                      <img
                        :src="selectedOrder.repair_proof_img"
                        alt="维修凭证"
                        class="w-full max-h-64 object-cover"
                      >
                    </button>
                    <div class="px-3 py-2 text-xs text-gray-500 border-t border-green-200 bg-white">
                      点击图片可放大查看
                    </div>
                  </div>
                  <p v-if="selectedOrder.repair_description" class="text-gray-900 whitespace-pre-wrap">
                    {{ selectedOrder.repair_description }}
                  </p>
                </div>
              </div>
              <div v-else-if="selectedOrder.status === 3" class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <h3 class="text-sm font-medium text-gray-700 mb-1">维修凭证</h3>
                <p class="text-sm text-gray-500">本工单未提交维修凭证图片/说明。</p>
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

              <!-- 用户评价 -->
              <div v-if="selectedOrder.comment" class="bg-amber-50 rounded-lg p-4">
                <div class="flex items-center justify-between gap-3 mb-2">
                  <h3 class="text-sm font-medium text-gray-700">评价</h3>
                  <div class="flex items-center gap-1">
                  <svg
                    v-for="i in 5"
                    :key="i"
                    class="w-5 h-5"
                    :class="i <= selectedOrder.comment.score ? 'text-amber-400' : 'text-gray-300'"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                  </svg>
                  </div>
                </div>
                <p v-if="selectedOrder.comment.feedback" class="text-gray-700 text-sm whitespace-pre-wrap">
                  {{ selectedOrder.comment.feedback }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 图片放大预览 -->
    <div
      v-if="imagePreviewUrl"
      class="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-[60]"
      @click="closeImagePreview"
    >
      <div class="max-w-5xl w-full max-h-[90vh]" @click.stop>
        <img
          :src="imagePreviewUrl"
          alt="图片预览"
          class="w-full h-full object-contain rounded-lg"
        >
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
const imagePreviewUrl = ref('')

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

function openImagePreview(url) {
  imagePreviewUrl.value = url || ''
}

function closeImagePreview() {
  imagePreviewUrl.value = ''
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
