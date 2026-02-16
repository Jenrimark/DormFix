<template>
  <div class="min-h-screen bg-bgLight">
    <AppNav v-if="!hideNav" />
    <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <Toast />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppNav from '@/components/AppNav.vue'
import Toast from '@/components/Toast.vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const userStore = useUserStore()
const hideNav = computed(() => route.meta.hideNav === true)

onMounted(() => {
  userStore.fetchUser()
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
