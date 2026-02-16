<template>
  <nav class="bg-white/90 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <router-link to="/" class="flex items-center space-x-3">
          <svg class="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          <span class="font-heading text-xl font-semibold text-textDark">DormFix</span>
        </router-link>
        <div class="flex items-center gap-4">
          <!-- Anchor links for homepage sections -->
          <a href="#features" class="text-gray-600 hover:text-primary transition-colors duration-200">功能</a>
          <a href="#demo" class="text-gray-600 hover:text-primary transition-colors duration-200">演示</a>
          
          <template v-if="userStore.isLoggedIn">
            <router-link to="/submit" class="text-gray-600 hover:text-primary transition-colors">提交报修</router-link>
            <router-link to="/orders" class="text-gray-600 hover:text-primary transition-colors">我的工单</router-link>
            <router-link v-if="userStore.isAdmin" to="/admin" class="text-gray-600 hover:text-primary transition-colors">管理后台</router-link>
            <router-link to="/profile" class="text-gray-600 hover:text-primary transition-colors">个人中心</router-link>
            <button type="button" @click="handleLogout" class="text-gray-600 hover:text-primary transition-colors">退出</button>
          </template>
          <template v-else>
            <router-link to="/login" class="text-gray-600 hover:text-primary transition-colors">登录</router-link>
            <router-link to="/register" class="px-4 py-2 bg-cta text-white rounded-lg hover:bg-cta/90 transition-colors cursor-pointer">注册</router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

async function handleLogout() {
  await userStore.logout()
  router.push('/')
}
</script>
