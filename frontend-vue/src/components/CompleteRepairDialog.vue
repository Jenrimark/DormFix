<template>
  <div @click="$emit('close')" 
    class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
    <div @click.stop class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <!-- 头部 -->
      <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
        <h2 class="font-heading text-xl font-bold text-textDark">完成维修</h2>
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
              <span class="text-gray-500">故障类型：</span>
              <span class="text-gray-900">{{ order.repair_type_info?.name }}</span>
            </div>
            <div class="col-span-2">
              <span class="text-gray-500">故障描述：</span>
              <span class="text-gray-900">{{ order.content }}</span>
            </div>
          </div>
        </div>

        <!-- 维修凭证表单 -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- 维修照片 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              维修凭证照片 <span class="text-gray-400">(选填)</span>
            </label>
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-primary transition-colors cursor-pointer"
              @click="$refs.fileInput.click()">
              <input ref="fileInput" type="file" accept="image/*" 
                @change="handleFileChange" class="hidden">
              
              <div v-if="!previewUrl">
                <svg class="w-12 h-12 mx-auto text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M12 4v16m8-8H4"></path>
                </svg>
                <p class="text-sm text-gray-600">点击上传维修照片</p>
                <p class="text-xs text-gray-400 mt-1">支持 JPG、PNG 格式</p>
              </div>
              
              <div v-else class="relative">
                <img :src="previewUrl" class="max-h-64 mx-auto rounded-lg">
                <button type="button" @click.stop="clearFile" 
                  class="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600 cursor-pointer">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- 维修说明 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              维修说明 <span class="text-red-500">*</span>
            </label>
            <textarea v-model="formData.repair_description" 
              placeholder="请详细描述维修过程和结果，例如：更换了损坏的水龙头，测试正常"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
              rows="4"
              required></textarea>
          </div>

          <!-- 耗材记录 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              耗材记录 <span class="text-gray-400">(选填)</span>
            </label>
            <textarea v-model="formData.materials" 
              placeholder="例如：水龙头 x1、生料带 x1"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
              rows="2"></textarea>
          </div>

          <!-- 提交按钮 -->
          <div class="flex gap-3 pt-4">
            <button type="button" @click="$emit('close')" 
              class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
              取消
            </button>
            <button type="submit" 
              :disabled="loading || (!formData.repair_description && !formData.repair_proof_img)"
              class="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed">
              <span v-if="loading">提交中...</span>
              <span v-else>✓ 确认完成</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { completeRepair } from '@/api'

const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'submit'])

const loading = ref(false)
const previewUrl = ref('')
const fileInput = ref(null)

const formData = reactive({
  repair_proof_img: null,
  repair_description: '',
  materials: ''
})

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.repair_proof_img = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

const clearFile = () => {
  formData.repair_proof_img = null
  previewUrl.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const handleSubmit = async () => {
  // 验证至少填写了维修说明或上传了照片
  if (!formData.repair_description.trim() && !formData.repair_proof_img) {
    alert('请至少填写维修说明或上传维修照片')
    return
  }
  
  loading.value = true
  
  try {
    // 创建 FormData 对象
    const data = new FormData()
    if (formData.repair_proof_img) {
      data.append('repair_proof_img', formData.repair_proof_img)
    }
    if (formData.repair_description.trim()) {
      data.append('repair_description', formData.repair_description.trim())
    }
    if (formData.materials.trim()) {
      data.append('materials', formData.materials.trim())
    }
    
    await completeRepair(props.order.id, data)
    
    alert('维修完成！')
    emit('submit')
    emit('close')
  } catch (error) {
    console.error('提交失败:', error)
    alert(error.response?.data?.error || '提交失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>
