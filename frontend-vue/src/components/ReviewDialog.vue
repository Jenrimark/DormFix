<template>
  <div @click="$emit('close')" 
    class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
    <div @click.stop class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <!-- 头部 -->
      <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
        <h2 class="font-heading text-xl font-bold text-textDark">审核工单</h2>
        <button @click="$emit('close')" 
          class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      
      <!-- 工单信息 -->
      <div class="p-6 space-y-4">
        <div class="bg-gray-50 rounded-lg p-4">
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-gray-500">工单编号：</span>
              <span class="text-gray-900 font-medium">{{ order.order_sn }}</span>
            </div>
            <div>
              <span class="text-gray-500">提交人：</span>
              <span class="text-gray-900">{{ order.user_info?.real_name || order.user_info?.username }}</span>
            </div>
            <div>
              <span class="text-gray-500">故障类型：</span>
              <span class="text-gray-900">{{ order.repair_type_info?.name }}</span>
            </div>
            <div>
              <span class="text-gray-500">紧急程度：</span>
              <span :class="priorityClass(order.priority)">{{ order.priority_display }}</span>
            </div>
            <div class="col-span-2">
              <span class="text-gray-500">提交时间：</span>
              <span class="text-gray-900">{{ order.create_time }}</span>
            </div>
          </div>
        </div>

        <!-- 故障描述 -->
        <div>
          <h3 class="text-sm font-medium text-gray-700 mb-2">故障描述</h3>
          <p class="text-gray-900 whitespace-pre-wrap bg-gray-50 rounded-lg p-3">{{ order.content }}</p>
        </div>

        <!-- 现场照片 -->
        <div v-if="order.img_proof">
          <h3 class="text-sm font-medium text-gray-700 mb-2">现场照片</h3>
          <img :src="order.img_proof" :alt="order.repair_type_info?.name" 
            class="w-full h-auto rounded-lg border border-gray-200">
        </div>

        <!-- 审核操作 -->
        <div class="border-t border-gray-200 pt-4">
          <h3 class="text-sm font-medium text-gray-700 mb-3">审核操作</h3>
          
          <div class="space-y-3">
            <!-- 审核备注 -->
            <div>
              <label class="block text-sm text-gray-600 mb-1">
                审核备注 <span v-if="action === 'reject'" class="text-red-500">*</span>
              </label>
              <textarea v-model="remark" 
                :placeholder="action === 'reject' ? '请填写拒绝原因（必填）' : '审核备注（选填）'"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
                rows="3"></textarea>
            </div>

            <!-- 操作按钮 -->
            <div class="flex gap-3">
              <button @click="handleSubmit('pass')" 
                :disabled="loading"
                class="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed">
                <span v-if="loading && action === 'pass'">审核中...</span>
                <span v-else>✓ 审核通过</span>
              </button>
              <button @click="handleSubmit('reject')" 
                :disabled="loading"
                class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed">
                <span v-if="loading && action === 'reject'">审核中...</span>
                <span v-else">✗ 审核拒绝</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { reviewOrder } from '@/api'
import { useNotification } from '@/composables/useNotification'

const { notify } = useNotification()
const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'submit'])

const remark = ref('')
const action = ref('')
const loading = ref(false)

const priorityClass = (priority) => {
  const classes = {
    'high': 'text-red-600 font-medium',
    'medium': 'text-orange-600',
    'low': 'text-gray-600'
  }
  return classes[priority] || 'text-gray-600'
}

const handleSubmit = async (actionType) => {
  action.value = actionType
  
  // 验证拒绝时必须填写原因
  if (actionType === 'reject' && !remark.value.trim()) {
    notify({
      message: '审核拒绝必须填写原因',
      type: 'warning'
    })
    return
  }
  
  loading.value = true
  
  try {
    await reviewOrder(props.order.id, {
      action: actionType,
      remark: remark.value.trim()
    })
    
    const message = actionType === 'pass' ? '审核通过' : '审核拒绝'
    notify({
      message,
      type: 'success'
    })
    emit('submit')
    emit('close')
  } catch (error) {
    console.error('审核失败:', error)
    notify({
      message: error.response?.data?.error || '审核失败，请重试',
      type: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>
