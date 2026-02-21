<template>
  <Teleport to="body">
    <Transition name="toast">
      <div
        v-if="visible"
        :class="['fixed top-20 left-1/2 -translate-x-1/2 z-[100] px-6 py-3 rounded-lg shadow-lg text-white', typeClass]"
      >
        {{ message }}
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const visible = ref(false)
const message = ref('')
const type = ref('info')
let timer = null

const typeClass = computed(() => ({
  success: 'bg-green-500',
  error: 'bg-red-500',
  info: 'bg-blue-500',
}[type.value]))

function show(msg, t = 'info') {
  message.value = msg
  type.value = t
  visible.value = true
  clearTimeout(timer)
  timer = setTimeout(() => {
    visible.value = false
  }, 3000)
}

onMounted(() => {
  window.__toast = show
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -1rem);
}
</style>
