<template>
  <button
    ref="buttonRef"
    :style="magneticStyle"
    @click="$emit('click')"
  >
    <slot></slot>
  </button>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useMediaQuery } from '@vueuse/core'

defineEmits(['click'])

const buttonRef = ref(null)
const offsetX = ref(0)
const offsetY = ref(0)
const isMobile = useMediaQuery('(max-width: 768px)')

const magneticStyle = computed(() => ({
  transform: `translate(${offsetX.value}px, ${offsetY.value}px)`,
  transition: 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)'
}))

const handleMouseMove = (e) => {
  if (isMobile.value || !buttonRef.value) return
  
  const rect = buttonRef.value.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2
  
  const deltaX = e.clientX - centerX
  const deltaY = e.clientY - centerY
  const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY)
  
  const maxDistance = 100
  const strength = 0.3
  
  if (distance < maxDistance) {
    offsetX.value = deltaX * strength
    offsetY.value = deltaY * strength
  } else {
    offsetX.value = 0
    offsetY.value = 0
  }
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
})
</script>
