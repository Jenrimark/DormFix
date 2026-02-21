<template>
  <div class="relative min-h-screen bg-space-purple text-white overflow-hidden">
    <!-- Dynamic Aurora Background -->
    <div class="fixed inset-0 -z-10">
      <div class="absolute inset-0 bg-gradient-to-br from-space-purple via-[#1a0b2e] to-space-purple animate-aurora"></div>
      <div 
        class="absolute inset-0 opacity-30 animate-aurora-slow"
        :style="gradientStyle"
      ></div>
    </div>

    <!-- Hero Section with Parallax -->
    <section class="relative min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <div 
        class="max-w-7xl mx-auto text-center"
        :style="parallaxStyle"
      >
        <!-- Giant Typography -->
        <h1 class="text-6xl sm:text-7xl md:text-8xl lg:text-9xl font-black leading-none mb-6">
          <span class="bg-gradient-to-r from-electric-purple via-fluorescent-cyan to-electric-purple bg-clip-text text-transparent animate-pulse">
            DormFix
          </span>
        </h1>
        
        <p class="text-xl sm:text-2xl md:text-3xl text-gray-300 mb-12 font-light">
          <span class="glass-text">基于 Django 的宿舍报修工单系统</span>
        </p>
        
        <!-- Magnetic Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <MagneticButton 
            @click="$router.push('/submit-order')"
            class="magnetic-btn-primary"
          >
            立即报修
          </MagneticButton>
          <MagneticButton 
            @click="$router.push('/order-tracking')"
            class="magnetic-btn-secondary"
          >
            查看工单
          </MagneticButton>
        </div>
      </div>
    </section>

    <!-- Stats Section with Counting Animation -->
    <section class="py-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <StatCard
            ref="stat1"
            :target="2.3"
            suffix="h"
            label="平均响应时间"
            :decimals="1"
          />
          <StatCard
            ref="stat2"
            :target="1500"
            suffix="+"
            label="已处理工单"
          />
          <StatCard
            ref="stat3"
            :target="98"
            suffix="%"
            label="学生满意度"
          />
        </div>
      </div>
    </section>

    <!-- Bento Grid with Spotlight Cards -->
    <section class="py-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-4xl sm:text-5xl font-bold text-white mb-12 text-center">
          核心功能
        </h2>
        
        <div class="bento-grid">
          <!-- Large Card -->
          <SpotlightCard class="bento-large" @click="$router.push('/submit-order')">
            <div class="flex items-start gap-4 h-full">
              <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-electric-purple to-fluorescent-cyan flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </div>
              <div class="flex-1">
                <h3 class="text-2xl font-bold text-white mb-3">快速提交报修</h3>
                <p class="text-gray-300 leading-relaxed">
                  简单几步即可提交报修申请，支持上传现场照片，实时跟踪工单状态
                </p>
              </div>
            </div>
          </SpotlightCard>
          
          <!-- Small Cards -->
          <SpotlightCard class="bento-small" @click="$router.push('/order-tracking')">
            <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-fluorescent-cyan to-electric-purple flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-white mb-2">实时跟踪</h3>
            <p class="text-gray-400 text-sm">随时查看工单进度</p>
          </SpotlightCard>
          
          <SpotlightCard class="bento-small" @click="$router.push('/admin')">
            <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-electric-purple to-fluorescent-cyan flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-white mb-2">智能派单</h3>
            <p class="text-gray-400 text-sm">自动分配维修人员</p>
          </SpotlightCard>
          
          <SpotlightCard class="bento-small">
            <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-fluorescent-cyan to-electric-purple flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-white mb-2">数据统计</h3>
            <p class="text-gray-400 text-sm">可视化数据分析</p>
          </SpotlightCard>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-8 text-center text-gray-400 border-t border-white/10">
      <p class="text-lg font-medium mb-2">DormFix - 基于 Django 的宿舍报修工单系统</p>
      <p class="text-sm">毕业设计项目 © 2026</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMouse, useWindowSize } from '@vueuse/core'
import MagneticButton from '@/components/MagneticButton.vue'
import SpotlightCard from '@/components/SpotlightCard.vue'
import StatCard from '@/components/StatCard.vue'

const { x: mouseX, y: mouseY } = useMouse()
const { width, height } = useWindowSize()

// Parallax effect
const parallaxStyle = computed(() => {
  const centerX = width.value / 2
  const centerY = height.value / 2
  const offsetX = ((mouseX.value - centerX) / centerX) * 20
  const offsetY = ((mouseY.value - centerY) / centerY) * 20
  
  return {
    transform: `translate(${offsetX}px, ${offsetY}px)`,
    transition: 'transform 0.3s ease-out'
  }
})

// Aurora gradient style
const gradientStyle = computed(() => ({
  background: `radial-gradient(circle at 20% 50%, rgba(168, 85, 247, 0.4) 0%, transparent 50%),
               radial-gradient(circle at 80% 80%, rgba(34, 211, 238, 0.4) 0%, transparent 50%)`
}))
</script>

<style scoped>
.glass-text {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 0.5rem 1.5rem;
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: inline-block;
}

.magnetic-btn-primary {
  @apply px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-300;
  @apply bg-gradient-to-r from-electric-purple to-fluorescent-cyan text-white;
  @apply hover:shadow-2xl hover:shadow-purple-500/50;
  cursor: pointer;
}

.magnetic-btn-secondary {
  @apply px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-300;
  @apply bg-white/5 backdrop-blur-lg text-white border border-white/10;
  @apply hover:bg-white/10 hover:shadow-2xl hover:shadow-cyan-500/30;
  cursor: pointer;
}

.bento-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .bento-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .bento-large {
    grid-column: span 2;
  }
}

@media (min-width: 1024px) {
  .bento-grid {
    grid-template-columns: repeat(3, 1fr);
    grid-auto-rows: 200px;
  }
  
  .bento-large {
    grid-column: span 2;
    grid-row: span 2;
  }
  
  .bento-small {
    grid-column: span 1;
    grid-row: span 1;
  }
}
</style>
