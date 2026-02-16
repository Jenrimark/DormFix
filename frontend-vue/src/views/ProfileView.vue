<template>
  <div class="max-w-xl mx-auto">
    <h1 class="font-heading text-2xl font-bold text-textDark mb-6">个人中心</h1>
    <div v-if="userStore.user" class="bg-white rounded-xl shadow-md p-6 space-y-4">
      <p><span class="text-gray-500">用户名：</span>{{ userStore.user.username }}</p>
      <p><span class="text-gray-500">角色：</span>{{ userStore.user.role_display }}</p>
      <p v-if="userStore.user.dorm_code"><span class="text-gray-500">宿舍：</span>{{ userStore.user.dorm_code }}</p>
      <p v-if="userStore.user.phone"><span class="text-gray-500">手机：</span>{{ userStore.user.phone }}</p>
      <p v-if="userStore.user.email"><span class="text-gray-500">邮箱：</span>{{ userStore.user.email }}</p>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>
