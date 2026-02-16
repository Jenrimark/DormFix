<template>
  <div class="min-h-[80vh] flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-6">
        <span class="font-heading text-2xl font-bold text-textDark">DormFix</span>
        <p class="text-gray-600 mt-1">注册账号</p>
      </div>
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <form @submit.prevent="onSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
            <input v-model="form.username" type="text" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
            <input v-model="form.email" type="email" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
            <input v-model="form.password" type="password" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">确认密码</label>
            <input v-model="form.password_confirm" type="password" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">角色</label>
            <select v-model.number="form.role" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary">
              <option :value="1">学生</option>
              <option :value="2">维修员</option>
              <option :value="3">管理员</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">手机号</label>
            <input v-model="form.phone" type="tel" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">宿舍号</label>
            <input v-model="form.dorm_code" type="text" placeholder="如 北一-305" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary" />
          </div>
          <button type="submit" :disabled="loading" class="w-full py-3 bg-cta text-white rounded-lg font-medium hover:bg-cta/90 disabled:opacity-50 cursor-pointer">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>
        <div class="mt-4 text-center text-gray-600 text-sm">
          已有账号？<router-link to="/login" class="text-primary font-medium">去登录</router-link>
        </div>
      </div>
      <div class="text-center mt-6">
        <router-link to="/" class="text-gray-600 hover:text-primary text-sm">← 返回首页</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  role: 1,
  phone: '',
  dorm_code: '',
})

async function onSubmit() {
  if (form.password !== form.password_confirm) {
    if (typeof window.__toast === 'function') window.__toast('两次密码不一致', 'error')
    return
  }
  loading.value = true
  try {
    await register(form)
    if (typeof window.__toast === 'function') window.__toast('注册成功，请登录', 'success')
    router.push('/login')
  } catch (e) {
    const msg = e.response?.data?.username?.[0] || e.response?.data?.email?.[0] || e.response?.data?.detail || '注册失败'
    if (typeof window.__toast === 'function') window.__toast(msg, 'error')
  } finally {
    loading.value = false
  }
}
</script>
