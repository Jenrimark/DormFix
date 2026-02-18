<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">提交报修工单</h1>
    <div class="bg-white rounded-xl shadow-md p-6">
      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">故障类型 <span class="text-red-500">*</span></label>
          <select v-model="form.repair_type" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary cursor-pointer">
            <option value="">请选择故障类型</option>
            <option v-for="t in repairTypes" :key="t.id" :value="t.id">{{ t.name }}</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">紧急程度 <span class="text-red-500">*</span></label>
          <select v-model="form.priority" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary cursor-pointer">
            <option value="low">不急 - 可以等待处理</option>
            <option value="medium">一般 - 尽快处理</option>
            <option value="high">紧急 - 需要立即处理</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">问题描述 <span class="text-red-500">*</span></label>
          <textarea v-model="form.content" required rows="4" maxlength="500" placeholder="请详细描述故障情况，包括位置、现象等信息"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary resize-none"></textarea>
          <p class="text-sm text-gray-500 mt-1">{{ form.content.length }}/500</p>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">现场照片（选填）</label>
          <div class="space-y-3">
            <!-- 图片预览 -->
            <div v-if="imagePreview" class="relative inline-block">
              <img :src="imagePreview" alt="预览图" class="w-full max-w-md h-auto rounded-lg border-2 border-gray-200">
              <button type="button" @click="removeImage" 
                class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 hover:bg-red-600 transition-colors cursor-pointer">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <!-- 上传按钮 -->
            <div v-if="!imagePreview" class="flex gap-3">
              <label class="flex-1 flex items-center justify-center px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary hover:bg-primary/5 transition-colors cursor-pointer">
                <svg class="w-5 h-5 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                <span class="text-sm text-gray-600">从相册选择</span>
                <input type="file" ref="fileInput" @change="onFileChange" accept="image/*" class="hidden">
              </label>
              
              <label class="flex-1 flex items-center justify-center px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary hover:bg-primary/5 transition-colors cursor-pointer">
                <svg class="w-5 h-5 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                <span class="text-sm text-gray-600">拍照上传</span>
                <input type="file" @change="onFileChange" accept="image/*" capture="environment" class="hidden">
              </label>
            </div>
            
            <p class="text-xs text-gray-500">支持 JPG、PNG 格式，文件大小不超过 5MB</p>
          </div>
        </div>
        
        <button type="submit" :disabled="loading" class="w-full py-3 bg-cta text-white rounded-lg font-medium hover:bg-cta/90 disabled:opacity-50 transition-colors cursor-pointer">
          {{ loading ? '提交中...' : '提交工单' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getRepairTypes, createWorkOrder } from '@/api'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const repairTypes = ref([])
const loading = ref(false)
const imagePreview = ref(null)
const imageFile = ref(null)
const fileInput = ref(null)

const form = reactive({
  repair_type: '',
  priority: 'medium',
  content: '',
})

onMounted(async () => {
  if (!userStore.user) {
    router.push({ name: 'Login', query: { redirect: '/submit' } })
    return
  }
  try {
    const { data } = await getRepairTypes()
    repairTypes.value = data
  } catch {
    if (typeof window.__toast === 'function') window.__toast('获取故障类型失败', 'error')
  }
})

function onFileChange(event) {
  const file = event.target.files[0]
  if (!file) return
  
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    if (typeof window.__toast === 'function') window.__toast('请选择图片文件', 'error')
    return
  }
  
  // 验证文件大小（5MB）
  if (file.size > 5 * 1024 * 1024) {
    if (typeof window.__toast === 'function') window.__toast('图片大小不能超过 5MB', 'error')
    return
  }
  
  imageFile.value = file
  
  // 生成预览
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
  }
  reader.readAsDataURL(file)
}

function removeImage() {
  imagePreview.value = null
  imageFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

async function onSubmit() {
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('repair_type', Number(form.repair_type))
    formData.append('priority', form.priority)
    formData.append('content', form.content.trim())
    
    if (imageFile.value) {
      formData.append('img_proof', imageFile.value)
    }
    
    await createWorkOrder(formData)
    if (typeof window.__toast === 'function') window.__toast('提交成功', 'success')
    router.push('/orders')
  } catch (e) {
    const msg = e.response?.data?.detail || '提交失败'
    if (typeof window.__toast === 'function') window.__toast(msg, 'error')
  } finally {
    loading.value = false
  }
}
</script>
