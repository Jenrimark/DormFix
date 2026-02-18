<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">个人中心</h1>
    
    <div v-if="userStore.user" class="space-y-6">
      <!-- 头像和基本信息卡片 -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <div class="flex items-start gap-6">
          <!-- 头像 -->
          <div class="flex-shrink-0">
            <div class="relative group">
              <img v-if="userStore.user.avatar_url" :src="userStore.user.avatar_url" 
                alt="头像" class="w-24 h-24 rounded-full object-cover border-4 border-gray-100">
              <div v-else class="w-24 h-24 rounded-full bg-primary/10 flex items-center justify-center border-4 border-gray-100">
                <span class="text-3xl font-bold text-primary">
                  {{ userStore.user.username.charAt(0).toUpperCase() }}
                </span>
              </div>
              
              <!-- 上传头像按钮 -->
              <label class="absolute inset-0 flex items-center justify-center bg-black/50 rounded-full opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                <input type="file" @change="selectAvatar" accept="image/*" class="hidden">
              </label>
            </div>
            <p class="text-xs text-gray-500 text-center mt-2">点击更换头像</p>
          </div>
          
          <!-- 用户信息 -->
          <div class="flex-1">
            <h2 class="text-xl font-bold text-gray-900">{{ userStore.user.real_name || userStore.user.username }}</h2>
            <p class="text-sm text-gray-500 mt-1">@{{ userStore.user.username }}</p>
            <div class="mt-3 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
              :class="roleClass">
              {{ userStore.user.role_display }}
            </div>
            <p v-if="userStore.user.bio" class="mt-3 text-gray-600">{{ userStore.user.bio }}</p>
          </div>
        </div>
      </div>

      <!-- 个人信息（全部可编辑，除了角色） -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-heading text-lg font-bold text-gray-900">个人信息</h3>
          <button v-if="!editing" @click="startEdit" 
            class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors cursor-pointer">
            编辑资料
          </button>
        </div>

        <form v-if="editing" @submit.prevent="saveProfile" class="space-y-4">
          <!-- 基本信息 -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">真实姓名</label>
              <input v-model="editForm.real_name" type="text" 
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">手机号</label>
              <input v-model="editForm.phone" type="tel" maxlength="11" 
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
            <input v-model="editForm.email" type="email" 
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
          </div>

          <!-- 学生专属字段 -->
          <div v-if="userStore.user.role === 1" class="border-t pt-4 mt-4">
            <h4 class="text-sm font-medium text-gray-700 mb-3">学籍信息</h4>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">学号</label>
                <input v-model="editForm.student_id" type="text" 
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">班号</label>
                <input v-model="editForm.class_number" type="text" 
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">学校</label>
                <input v-model="editForm.school" type="text" 
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">校区</label>
                <input v-model="editForm.campus" type="text" 
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
              </div>

              <div class="col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">宿舍号</label>
                <input v-model="editForm.dorm_code" type="text" 
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">个人简介</label>
            <textarea v-model="editForm.bio" rows="3" maxlength="200"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary resize-none"></textarea>
            <p class="text-sm text-gray-500 mt-1">{{ editForm.bio?.length || 0 }}/200</p>
          </div>

          <div class="flex gap-3">
            <button type="submit" :disabled="saving"
              class="flex-1 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50 transition-colors cursor-pointer">
              {{ saving ? '保存中...' : '保存' }}
            </button>
            <button type="button" @click="cancelEdit"
              class="flex-1 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer">
              取消
            </button>
          </div>
        </form>

        <div v-else class="space-y-3">
          <div class="flex items-center gap-3 py-2">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            <span class="text-sm text-gray-500 w-20">真实姓名</span>
            <span class="text-gray-900">{{ userStore.user.real_name || '未设置' }}</span>
          </div>
          <div class="flex items-center gap-3 py-2">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
            <span class="text-sm text-gray-500 w-20">邮箱</span>
            <span class="text-gray-900">{{ userStore.user.email || '未设置' }}</span>
          </div>
          <div class="flex items-center gap-3 py-2">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
            </svg>
            <span class="text-sm text-gray-500 w-20">手机号</span>
            <span class="text-gray-900">{{ userStore.user.phone || '未设置' }}</span>
          </div>

          <!-- 学生信息显示 -->
          <div v-if="userStore.user.role === 1" class="border-t pt-3 mt-3">
            <div class="flex items-center gap-3 py-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>
              </svg>
              <span class="text-sm text-gray-500 w-20">学号</span>
              <span class="text-gray-900">{{ userStore.user.student_id || '未设置' }}</span>
            </div>
            <div class="flex items-center gap-3 py-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
              <span class="text-sm text-gray-500 w-20">学校</span>
              <span class="text-gray-900">{{ userStore.user.school || '未设置' }}</span>
            </div>
            <div class="flex items-center gap-3 py-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
              <span class="text-sm text-gray-500 w-20">校区</span>
              <span class="text-gray-900">{{ userStore.user.campus || '未设置' }}</span>
            </div>
            <div class="flex items-center gap-3 py-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
              </svg>
              <span class="text-sm text-gray-500 w-20">班号</span>
              <span class="text-gray-900">{{ userStore.user.class_number || '未设置' }}</span>
            </div>
            <div class="flex items-center gap-3 py-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
              </svg>
              <span class="text-sm text-gray-500 w-20">宿舍号</span>
              <span class="text-gray-900">{{ userStore.user.dorm_code || '未设置' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 账号信息 -->
      <div class="bg-white rounded-xl shadow-md p-6">
        <h3 class="font-heading text-lg font-bold text-gray-900 mb-4">账号信息</h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between py-2 bg-gray-50 px-4 rounded-lg">
            <div class="flex items-center gap-3">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
              </svg>
              <div>
                <span class="text-gray-900 font-medium">角色权限</span>
                <p class="text-xs text-gray-500">系统分配，不可修改</p>
              </div>
            </div>
            <div class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
              :class="roleClass">
              {{ userStore.user.role_display }}
            </div>
          </div>
          <div class="flex items-center justify-between py-2">
            <div class="flex items-center gap-3">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>
              <span class="text-gray-900">修改密码</span>
            </div>
            <button @click="showPasswordModal = true"
              class="text-primary hover:text-primary/80 transition-colors cursor-pointer">
              修改
            </button>
          </div>
          <div class="flex items-center justify-between py-2">
            <div class="flex items-center gap-3">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              <span class="text-gray-900">注册时间</span>
            </div>
            <span class="text-gray-500">{{ userStore.user.created_at }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 头像裁剪弹窗 -->
    <AvatarCropper 
      :show="showCropper" 
      :imageFile="selectedImage"
      @close="showCropper = false"
      @cropped="uploadCroppedAvatar"
    />

    <!-- 修改密码弹窗 -->
    <div v-if="showPasswordModal" @click="showPasswordModal = false"
      class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div @click.stop class="bg-white rounded-xl max-w-md w-full p-6">
        <h3 class="font-heading text-xl font-bold text-gray-900 mb-4">修改密码</h3>
        <form @submit.prevent="changePassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">旧密码</label>
            <input v-model="passwordForm.old_password" type="password" required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">新密码</label>
            <input v-model="passwordForm.new_password" type="password" required minlength="6"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">确认新密码</label>
            <input v-model="passwordForm.new_password_confirm" type="password" required minlength="6"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary">
          </div>
          <div class="flex gap-3">
            <button type="submit" :disabled="changingPassword"
              class="flex-1 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50 transition-colors cursor-pointer">
              {{ changingPassword ? '修改中...' : '确认修改' }}
            </button>
            <button type="button" @click="showPasswordModal = false"
              class="flex-1 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer">
              取消
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { updateProfile, uploadAvatar, changePassword as changePasswordApi } from '@/api'
import AvatarCropper from '@/components/AvatarCropper.vue'

const userStore = useUserStore()
const editing = ref(false)
const saving = ref(false)
const showPasswordModal = ref(false)
const changingPassword = ref(false)
const showCropper = ref(false)
const selectedImage = ref(null)

const editForm = reactive({
  real_name: '',
  email: '',
  phone: '',
  bio: '',
  student_id: '',
  school: '',
  campus: '',
  class_number: '',
  dorm_code: ''
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
})

const roleClass = computed(() => {
  const classes = {
    1: 'bg-blue-100 text-blue-700',
    2: 'bg-green-100 text-green-700',
    3: 'bg-purple-100 text-purple-700'
  }
  return classes[userStore.user?.role] || 'bg-gray-100 text-gray-700'
})

function startEdit() {
  editForm.real_name = userStore.user.real_name || ''
  editForm.email = userStore.user.email || ''
  editForm.phone = userStore.user.phone || ''
  editForm.bio = userStore.user.bio || ''
  editForm.student_id = userStore.user.student_id || ''
  editForm.school = userStore.user.school || ''
  editForm.campus = userStore.user.campus || ''
  editForm.class_number = userStore.user.class_number || ''
  editForm.dorm_code = userStore.user.dorm_code || ''
  editing.value = true
}

function cancelEdit() {
  editing.value = false
}

async function saveProfile() {
  saving.value = true
  try {
    const { data } = await updateProfile(editForm)
    userStore.setUser(data.user)
    editing.value = false
    if (typeof window.__toast === 'function') {
      window.__toast('个人信息更新成功', 'success')
    }
  } catch (error) {
    const errorMsg = error.response?.data?.error || error.message || '更新失败'
    if (typeof window.__toast === 'function') {
      window.__toast(errorMsg, 'error')
    }
  } finally {
    saving.value = false
  }
}

async function handleAvatarUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    if (typeof window.__toast === 'function') {
      window.__toast('请选择图片文件', 'error')
    }
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    if (typeof window.__toast === 'function') {
      window.__toast('图片大小不能超过 5MB', 'error')
    }
    return
  }

  const formData = new FormData()
  formData.append('avatar', file)

  try {
    const { data } = await uploadAvatar(formData)
    userStore.setUser(data.user)
    if (typeof window.__toast === 'function') {
      window.__toast('头像上传成功', 'success')
    }
  } catch (error) {
    const errorMsg = error.response?.data?.error || error.message || '上传失败'
    if (typeof window.__toast === 'function') {
      window.__toast(errorMsg, 'error')
    }
  }
}

function selectAvatar(event) {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    if (typeof window.__toast === 'function') {
      window.__toast('请选择图片文件', 'error')
    }
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    if (typeof window.__toast === 'function') {
      window.__toast('图片大小不能超过 5MB', 'error')
    }
    return
  }

  selectedImage.value = file
  showCropper.value = true
  
  // 清空 input，允许选择同一文件
  event.target.value = ''
}

async function uploadCroppedAvatar(blob) {
  showCropper.value = false

  const formData = new FormData()
  formData.append('avatar', blob, 'avatar.jpg')

  try {
    const { data } = await uploadAvatar(formData)
    userStore.setUser(data.user)
    if (typeof window.__toast === 'function') {
      window.__toast('头像上传成功', 'success')
    }
  } catch (error) {
    const errorMsg = error.response?.data?.error || error.message || '上传失败'
    if (typeof window.__toast === 'function') {
      window.__toast(errorMsg, 'error')
    }
  }
}

async function changePassword() {
  if (passwordForm.new_password !== passwordForm.new_password_confirm) {
    if (typeof window.__toast === 'function') {
      window.__toast('两次新密码不一致', 'error')
    }
    return
  }

  changingPassword.value = true
  try {
    await changePasswordApi(passwordForm)
    showPasswordModal.value = false
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.new_password_confirm = ''
    if (typeof window.__toast === 'function') {
      window.__toast('密码修改成功', 'success')
    }
  } catch (error) {
    const errorMsg = error.response?.data?.error || error.message || '修改失败'
    if (typeof window.__toast === 'function') {
      window.__toast(errorMsg, 'error')
    }
  } finally {
    changingPassword.value = false
  }
}
</script>
