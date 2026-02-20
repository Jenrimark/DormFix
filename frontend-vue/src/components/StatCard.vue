<template>
  <div ref="cardRef" class="glass-card p-8 text-center">
    <div class="text-5xl font-black mb-2 gradient-text">
      {{ displayCount }}{{ suffix }}
    </div>
    <div class="text-gray-400 text-lg">{{ label }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useIntersectionObserver } from '@vueuse/core'

const props = defineProps({
  target: {
    type: Number,
    required: true
  },
  suffix: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    required: true
  },
  decimals: {
    type: Number,
    default: 0
  }
})

const cardRef = ref(null)
const count = ref(0)
const hasAnimated = ref(false)

const displayCount = computed(() => {
  return count.value.toFixed(props.decimals)
})

const startCounting = () => {
  if (hasAnimated.value) return
  
  const duration = 2000
  const startTime = Date.now()
  const startValue = 0
  
  const animate = () => {
    const elapsed = Date.now() - startTime
    const progress = Math.min(elapsed / duration, 1)
    
    // Easing function (ease-out-quad)
    const easedProgress = progress * (2 - progress)
    
    count.value = startValue + (props.target - startValue) * easedProgress
    
    if (progress < 1) {
      requestAnimationFrame(animate)
    } else {
      hasAnimated.value = true
    }
  }
  
  animate()
}

onMounted(() => {
  useIntersectionObserver(
    cardRef,
    ([{ isIntersecting }]) => {
      if (isIntersecting && !hasAnimated.value) {
        startCounting()
      }
    },
    { threshold: 0.5 }
  )
})
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
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(168, 85, 247, 0.2);
}

.gradient-text {
  background: linear-gradient(135deg, #A855F7, #22D3EE);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 900;
}
</style>
