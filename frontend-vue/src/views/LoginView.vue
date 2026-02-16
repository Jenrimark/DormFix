<template>
  <div class="min-h-[80vh] flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="inline-flex items-center gap-3 mb-4">
          <svg class="w-12 h-12 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          <span class="font-heading text-3xl font-bold text-textDark">DormFix</span>
        </div>
        <p class="text-gray-600">宿舍报修工单管理系统</p>
      </div>
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <h2 class="font-heading text-2xl font-bold text-textDark mb-6 text-center">登录账号</h2>
        <form @submit.prevent="onSubmit" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
            <input v-model="form.username" type="text" required placeholder="请输入用户名"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">密码</label>
            <input v-model="form.password" :type="showPwd ? 'text' : 'password'" required placeholder="请输入密码"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent" />
            <button type="button" @click="showPwd = !showPwd" class="mt-2 text-sm text-gray-500 hover:text-gray-700">切换显示</button>
          </div>
          <button type="submit" :disabled="loading"
            class="w-full px-6 py-3 bg-cta text-white rounded-lg font-medium hover:bg-cta/90 transition-all disabled:opacity-50 cursor-pointer">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>
        <div class="mt-6 text-center text-gray-600">
          还没有账号？<router-link to="/register" class="text-primary font-medium ml-1">立即注册</router-link>
        </div>
      </div>
      <div class="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-800">
        <p class="font-medium mb-2">测试账号</p>
        <p>学生: student1 / student123</p>
        <p>维修员: repairman1 / repair123</p>
        <p>管理员: admin / admin123</p>
      </div>
      <div class="text-center mt-6">
        <router-link to="/" class="text-gray-600 hover:text-primary text-sm">← 返回首页</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const showPwd = ref(false)
const loading = ref(false)
const form = reactive({ username: '', password: '' })

async function onSubmit() {
  loading.value = true
  try {
    await userStore.login(form)
    if (typeof window.__toast === 'function') window.__toast('登录成功', 'success')
    const redirect = route.query.redirect || (userStore.user?.role === 3 ? '/admin' : userStore.user?.role === 2 ? '/orders' : '/orders')
    router.push(redirect)
  } catch (e) {
    const msg = e.response?.data?.error || '登录失败，请检查用户名和密码'
    if (typeof window.__toast === 'function') window.__toast(msg, 'error')
  } finally {
    loading.value = false
  }
}
</script>
