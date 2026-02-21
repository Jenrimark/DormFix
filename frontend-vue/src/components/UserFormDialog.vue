<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="handleClose">
    <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-4">
      <div class="flex justify-between items-center p-6 border-b border-gray-200">
        <h2 class="font-heading text-xl font-bold text-textDark">
          {{ isEditMode ? '编辑用户' : '创建用户' }}
        </h2>
        <button @click="handleClose" class="text-gray-400 hover:text-gray-600 cursor-pointer">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            用户名 <span class="text-red-500">*</span>
          </label>
          <input
            v-model="formData.username"
            type="text"
            :disabled="isEditMode"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary disabled:bg-gray-100"
            placeholder="请输入用户名"
          />
        </div>

        <div v-if="!isEditMode">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            密码 <span class="text-red-500">*</span>
          </label>
          <input
            v-model="formData.password"
            type="password"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="请输入密码"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            姓名 <span class="text-red-500">*</span>
          </label>
          <input
            v-model="formData.real_name"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="请输入姓名"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            角色 <span class="text-red-500">*</span>
          </label>
          <select
            v-model="formData.role"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary cursor-pointer"
          >
            <option value="">请选择角色</option>
            <option value="1">学生</option>
            <option value="2">维修人员</option>
            <option value="3">管理员</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">手机号</label>
          <input
            v-model="formData.phone"
            type="tel"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="请输入手机号"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
          <input
            v-model="formData.email"
            type="email"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="请输入邮箱"
          />
        </div>

        <div class="flex justify-end gap-3 pt-4">
          <button
            type="button"
            @click="handleClose"
            class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="submitting"
            class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {{ submitting ? '提交中...' : (isEditMode ? '保存' : '创建') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { createUser, updateUser } from '@/api'
import { useNotification } from '@/composables/useNotification'

const { notify } = useNotification()
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  user: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'success'])

const isEditMode = ref(false)
const submitting = ref(false)
const formData = ref({
  username: '',
  password: '',
  real_name: '',
  role: '',
  phone: '',
  email: ''
})

watch(() => props.user, (newUser) => {
  if (newUser) {
    isEditMode.value = true
    formData.value = {
      username: newUser.username || '',
      password: '',
      real_name: newUser.real_name || '',
      role: String(newUser.role) || '',
      phone: newUser.phone || '',
      email: newUser.email || ''
    }
  } else {
    isEditMode.value = false
    resetForm()
  }
}, { immediate: true })

function resetForm() {
  formData.value = {
    username: '',
    password: '',
    real_name: '',
    role: '',
    phone: '',
    email: ''
  }
}

function handleClose() {
  emit('close')
  resetForm()
}

async function handleSubmit() {
  submitting.value = true
  try {
    const data = {
      ...formData.value,
      role: parseInt(formData.value.role)
    }

    if (isEditMode.value) {
      // 编辑模式：不发送密码字段
      delete data.password
      await updateUser(props.user.id, data)
      notify({
        message: '用户更新成功',
        type: 'success'
      })
    } else {
      // 创建模式：需要密码
      if (!data.password) {
        notify({
          message: '请输入密码',
          type: 'warning'
        })
        return
      }
      await createUser(data)
      notify({
        message: '用户创建成功',
        type: 'success'
      })
    }

    emit('success')
    handleClose()
  } catch (error) {
    console.error('提交失败:', error)
    const errorMsg = error.response?.data?.error || error.response?.data?.username?.[0] || '操作失败'
    notify({
      message: errorMsg,
      type: 'error'
    })
  } finally {
    submitting.value = false
  }
}
</script>
