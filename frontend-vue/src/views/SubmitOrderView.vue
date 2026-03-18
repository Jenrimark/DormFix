<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">提交报修工单</h1>
    <div class="bg-white rounded-xl shadow-md p-6">
      <form @submit.prevent="onSubmit" class="space-y-4">
        <!-- 故障类型 - 选择类别 -->
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">故障类别 <span class="text-red-500">*</span></label>
            <div class="grid grid-cols-1 gap-3">
              <label 
                v-for="cat in categoryOptions" 
                :key="cat.value"
                class="flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all"
                :class="{
                  'border-primary bg-primary/5': form.category === cat.value,
                  'border-red-200 bg-red-50': cat.priority === 'high' && form.category !== cat.value,
                  'border-yellow-200 bg-yellow-50': cat.priority === 'medium' && form.category !== cat.value,
                  'border-gray-200 hover:border-primary/50 hover:bg-gray-50': cat.priority === 'low' && form.category !== cat.value
                }"
              >
                <input 
                  type="radio" 
                  :value="cat.value" 
                  v-model="form.category"
                  @change="onCategorySelect(cat)"
                  class="sr-only"
                >
                <div class="flex items-center gap-3 flex-1">
                  <div class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                    <span class="text-xl">{{ cat.icon }}</span>
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center gap-2">
                      <h3 class="font-medium text-gray-900">{{ cat.label }}</h3>
                      <span 
                        v-if="cat.priority === 'high'" 
                        class="px-2 py-0.5 text-xs font-medium bg-red-100 text-red-700 rounded-full"
                      >
                        紧急
                      </span>
                      <span 
                        v-else-if="cat.priority === 'medium'" 
                        class="px-2 py-0.5 text-xs font-medium bg-yellow-100 text-yellow-700 rounded-full"
                      >
                        一般
                      </span>
                      <span 
                        v-else 
                        class="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-600 rounded-full"
                      >
                        不急
                      </span>
                    </div>
                    <p class="text-xs text-gray-500 mt-1">{{ cat.description }}</p>
                  </div>
                </div>
              </label>
            </div>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">紧急程度 <span class="text-red-500">*</span></label>
          <div class="grid grid-cols-3 gap-3">
            <label 
              class="flex flex-col items-center p-3 border-2 rounded-lg cursor-pointer transition-all"
              :class="{
                'border-red-500 bg-red-50': form.priority === 'high',
                'border-gray-200 hover:border-red-300': form.priority !== 'high'
              }"
            >
              <input type="radio" value="high" v-model="form.priority" class="sr-only">
              <span class="text-2xl mb-1">🚨</span>
              <span class="text-sm font-medium">紧急</span>
              <span class="text-xs text-gray-500 mt-1">立即处理</span>
            </label>
            
            <label 
              class="flex flex-col items-center p-3 border-2 rounded-lg cursor-pointer transition-all"
              :class="{
                'border-yellow-500 bg-yellow-50': form.priority === 'medium',
                'border-gray-200 hover:border-yellow-300': form.priority !== 'medium'
              }"
            >
              <input type="radio" value="medium" v-model="form.priority" class="sr-only">
              <span class="text-2xl mb-1">⚠️</span>
              <span class="text-sm font-medium">一般</span>
              <span class="text-xs text-gray-500 mt-1">尽快处理</span>
            </label>
            
            <label 
              class="flex flex-col items-center p-3 border-2 rounded-lg cursor-pointer transition-all"
              :class="{
                'border-green-500 bg-green-50': form.priority === 'low',
                'border-gray-200 hover:border-green-300': form.priority !== 'low'
              }"
            >
              <input type="radio" value="low" v-model="form.priority" class="sr-only">
              <span class="text-2xl mb-1">✅</span>
              <span class="text-sm font-medium">不急</span>
              <span class="text-xs text-gray-500 mt-1">可以等待</span>
            </label>
          </div>
          <p v-if="autoSetPriority" class="text-xs text-blue-600 mt-2">
            💡 已根据故障类型自动设置为"{{ priorityText }}"
          </p>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getRepairTypes, createWorkOrder } from '@/api'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const autoSetPriority = ref(false)
const loading = ref(false)
const imagePreview = ref(null)
const imageFile = ref(null)
const fileInput = ref(null)

const form = reactive({
  category: '',
  priority: 'medium',
  content: '',
})

// 类别选项配置
const categoryOptions = [
  { 
    value: '水电', 
    label: '水电类', 
    icon: '💧',
    description: '漏水、断电、照明等问题',
    priority: 'high'
  },
  { 
    value: '网络', 
    label: '网络类', 
    icon: '📡',
    description: '网络故障、网口损坏等',
    priority: 'high'
  },
  { 
    value: '家具', 
    label: '家具类', 
    icon: '🪑',
    description: '床、桌椅、柜子等家具问题',
    priority: 'medium'
  },
  { 
    value: '门窗', 
    label: '门窗类', 
    icon: '🚪',
    description: '门锁、窗户、玻璃等问题',
    priority: 'medium'
  },
  { 
    value: '其他', 
    label: '其他', 
    icon: '🔧',
    description: '其他类型的报修',
    priority: 'low'
  }
]

// 计算属性：优先级文本
const priorityText = computed(() => {
  const map = { high: '紧急', medium: '一般', low: '不急' }
  return map[form.priority] || '一般'
})

// 选择类别时自动设置优先级
function onCategorySelect(cat) {
  form.priority = cat.priority
  autoSetPriority.value = true
  
  // 3秒后隐藏提示
  setTimeout(() => {
    autoSetPriority.value = false
  }, 3000)
}

onMounted(async () => {
  if (!userStore.user) {
    router.push({ name: 'Login', query: { redirect: '/submit' } })
    return
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
    formData.append('category', form.category)
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

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}

/* 隐藏原生单选按钮但保持可访问性 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>