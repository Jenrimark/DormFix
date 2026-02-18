<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">调试信息</h1>
    
    <div class="space-y-4">
      <!-- 用户状态 -->
      <div class="bg-white rounded-lg shadow p-4">
        <h2 class="font-bold mb-2">用户状态</h2>
        <pre class="bg-gray-100 p-3 rounded text-sm overflow-auto">{{ userInfo }}</pre>
      </div>
      
      <!-- 故障类型 -->
      <div class="bg-white rounded-lg shadow p-4">
        <h2 class="font-bold mb-2">故障类型数据</h2>
        <button @click="fetchRepairTypes" class="mb-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
          重新获取故障类型
        </button>
        <pre class="bg-gray-100 p-3 rounded text-sm overflow-auto">{{ repairTypesInfo }}</pre>
      </div>
      
      <!-- Cookie 信息 -->
      <div class="bg-white rounded-lg shadow p-4">
        <h2 class="font-bold mb-2">Cookie 信息</h2>
        <pre class="bg-gray-100 p-3 rounded text-sm overflow-auto">{{ cookieInfo }}</pre>
      </div>
      
      <!-- 测试登录 -->
      <div class="bg-white rounded-lg shadow p-4">
        <h2 class="font-bold mb-2">测试登录</h2>
        <div class="flex gap-2 mb-2">
          <input v-model="testUsername" placeholder="用户名" class="border px-3 py-2 rounded">
          <input v-model="testPassword" type="password" placeholder="密码" class="border px-3 py-2 rounded">
          <button @click="testLogin" class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
            测试登录
          </button>
        </div>
        <pre class="bg-gray-100 p-3 rounded text-sm overflow-auto">{{ loginResult }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getRepairTypes, login } from '@/api'

const userStore = useUserStore()
const repairTypes = ref([])
const repairTypesError = ref(null)
const testUsername = ref('student1')
const testPassword = ref('student123')
const loginResult = ref('未测试')

const userInfo = computed(() => ({
  isLoggedIn: userStore.isLoggedIn,
  user: userStore.user,
  isAdmin: userStore.isAdmin,
  isRepairman: userStore.isRepairman
}))

const repairTypesInfo = computed(() => ({
  count: repairTypes.value.length,
  data: repairTypes.value,
  error: repairTypesError.value
}))

const cookieInfo = computed(() => {
  const cookies = document.cookie.split(';').reduce((acc, cookie) => {
    const [key, value] = cookie.trim().split('=')
    acc[key] = value
    return acc
  }, {})
  return {
    all: document.cookie,
    parsed: cookies,
    hasSessionId: !!cookies.sessionid,
    hasCsrfToken: !!cookies.csrftoken
  }
})

async function fetchRepairTypes() {
  try {
    repairTypesError.value = null
    const { data } = await getRepairTypes()
    // 处理分页数据
    repairTypes.value = data.results || data
  } catch (error) {
    repairTypesError.value = {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status
    }
  }
}

async function testLogin() {
  try {
    const result = await login({
      username: testUsername.value,
      password: testPassword.value
    })
    loginResult.value = {
      success: true,
      data: result.data
    }
    // 刷新用户信息
    await userStore.fetchUser()
  } catch (error) {
    loginResult.value = {
      success: false,
      error: error.message,
      response: error.response?.data
    }
  }
}

onMounted(async () => {
  await fetchRepairTypes()
})
</script>
