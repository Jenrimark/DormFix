<template>
  <div 
    ref="cardRef"
    class="relative group cursor-pointer overflow-hidden rounded-2xl"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <!-- Spotlight overlay -->
    <div 
      v-if="!isMobile && isHovered"
      class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
      :style="spotlightStyle"
    ></div>
    
    <!-- Glass card -->
    <div class="relative glass-card p-6 sm:p-8 h-full">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useMediaQuery } from '@vueuse/core'

const cardRef = ref(null)
const mouseX = ref(0)
const mouseY = ref(0)
const isHovered = ref(false)
const isMobile = useMediaQuery('(max-width: 768px)')

const handleMouseMove = (e) => {
  if (!cardRef.value) return
  
  const rect = cardRef.value.getBoundingClientRect()
  mouseX.value = e.clientX - rect.left
  mouseY.value = e.clientY - rect.top
  isHovered.value = true
}

const handleMouseLeave = () => {
  isHovered.value = false
}

const spotlightStyle = computed(() => ({
  background: `radial-gradient(circle 200px at ${mouseX.value}px ${mouseY.value}px, rgba(168, 85, 247, 0.3), transparent)`,
  border: `1px solid rgba(168, 85, 247, 0.5)`
}))
</script>

<style scoped>
.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  transition: all 0.3s ease;
}

.glass-card:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(168, 85, 247, 0.4);
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(168, 85, 247, 0.2);
}

/* Fallback for browsers without backdrop-filter support */
@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.15);
  }
}
</style>
