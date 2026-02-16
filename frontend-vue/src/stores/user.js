import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getMe, login as apiLogin, logout as apiLogout } from '@/api'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)

  const isLoggedIn = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 3)
  const isRepairman = computed(() => user.value?.role === 2)

  async function fetchUser() {
    try {
      const { data } = await getMe()
      user.value = data
      return data
    } catch {
      user.value = null
      return null
    }
  }

  async function login(credentials) {
    const { data } = await apiLogin(credentials)
    user.value = data.user
    return data
  }

  async function logout() {
    await apiLogout()
    user.value = null
  }

  function setUser(u) {
    user.value = u
  }

  return { user, isLoggedIn, isAdmin, isRepairman, fetchUser, login, logout, setUser }
})
