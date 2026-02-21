<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 via-white to-cyan-50">
    <!-- Hero Section - Full Screen -->
    <section class="relative min-h-screen flex items-center justify-center overflow-hidden">
      <!-- Animated Background Elements -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute top-20 left-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div class="absolute top-40 right-10 w-72 h-72 bg-cyan-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div class="absolute -bottom-8 left-1/2 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <!-- Main Content -->
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <!-- Badge -->
        <div class="inline-flex items-center px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full shadow-lg mb-8 animate-fade-in-down">
          <span class="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
          <span class="text-sm font-medium gradient-text">基于 Django 的智能报修系统</span>
        </div>

        <!-- Main Title -->
        <h1 class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-black mb-6 animate-fade-in-up">
          <span class="gradient-text-large">DormFix</span>
        </h1>

        <!-- Subtitle -->
        <div class="mb-12 animate-fade-in-up animation-delay-200">
          <p class="text-2xl sm:text-3xl md:text-4xl text-gray-800 mb-6 font-semibold tracking-tight">
            让宿舍报修更<span class="gradient-text-large">简单</span>、更<span class="gradient-text-large">高效</span>
          </p>
          
          <div class="flex flex-wrap justify-center gap-3 sm:gap-4 max-w-3xl mx-auto text-base sm:text-lg">
            <span class="animate-float inline-flex items-center px-4 py-2 bg-gradient-to-r from-purple-100 to-purple-50 text-purple-700 rounded-full font-medium shadow-sm hover:shadow-md transition-shadow duration-300">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              全流程数字化
            </span>
            <span class="animate-float inline-flex items-center px-4 py-2 bg-gradient-to-r from-cyan-100 to-cyan-50 text-cyan-700 rounded-full font-medium shadow-sm hover:shadow-md transition-shadow duration-300">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              实时跟踪
            </span>
            <span class="animate-float inline-flex items-center px-4 py-2 bg-gradient-to-r from-pink-100 to-pink-50 text-pink-700 rounded-full font-medium shadow-sm hover:shadow-md transition-shadow duration-300">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
              智能派单
            </span>
            <span class="animate-float inline-flex items-center px-4 py-2 bg-gradient-to-r from-indigo-100 to-indigo-50 text-indigo-700 rounded-full font-medium shadow-sm hover:shadow-md transition-shadow duration-300">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path>
              </svg>
              数据可视化
            </span>
          </div>
        </div>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center mb-16 animate-fade-in-up animation-delay-400">
          <button @click="scrollToSection('notification')" class="group relative px-8 py-4 bg-gradient-to-r from-purple-600 to-cyan-600 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 cursor-pointer">
            <span class="relative z-10">通知中心</span>
            <div class="absolute inset-0 bg-gradient-to-r from-purple-700 to-cyan-700 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </button>
          <button @click="scrollToSection('features')" class="px-8 py-4 bg-white text-gray-800 rounded-xl font-semibold text-lg shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 border-2 border-gray-200 hover:border-purple-300 cursor-pointer">
            核心功能
          </button>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-4xl mx-auto mb-16 animate-fade-in-up animation-delay-600">
          <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transform hover:-translate-y-2 transition-all duration-300">
            <div class="text-4xl font-black gradient-text-large mb-2">2.3h</div>
            <div class="text-gray-600 font-medium">平均响应时间</div>
          </div>
          <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transform hover:-translate-y-2 transition-all duration-300">
            <div class="text-4xl font-black gradient-text-large mb-2">4.5h</div>
            <div class="text-gray-600 font-medium">平均报修时长</div>
          </div>
          <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transform hover:-translate-y-2 transition-all duration-300">
            <div class="text-4xl font-black gradient-text-large mb-2">98%</div>
            <div class="text-gray-600 font-medium">学生满意度</div>
          </div>
        </div>

        <!-- Scroll Indicator -->
        <div class="flex justify-center animate-bounce">
          <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
          </svg>
        </div>
      </div>
    </section>

    <!-- Notification Section -->
    <section id="notification" class="py-20 px-4 sm:px-6 lg:px-8 bg-white">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl sm:text-5xl font-bold mb-4">
            <span class="gradient-text-large">通知中心</span>
          </h2>
          <p class="text-xl text-gray-600">系统公告与重要提醒</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- System Announcements -->
          <div class="bg-white rounded-2xl p-8 shadow-lg border border-purple-100">
            <div class="flex items-center mb-6">
              <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mr-4">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">系统公告</h3>
            </div>
            
            <div class="space-y-4">
              <div 
                v-for="(announcement, index) in announcements" 
                :key="announcement.id"
                class="group p-4 rounded-xl bg-gradient-to-r hover:from-purple-100 transition-all duration-300 cursor-pointer border-l-4"
                :class="{
                  'from-purple-50 to-transparent border-purple-500': index === 0,
                  'from-cyan-50 to-transparent border-cyan-500': index === 1,
                  'from-pink-50 to-transparent border-pink-500': index === 2
                }"
              >
                <div class="flex items-start justify-between mb-2">
                  <h4 
                    class="font-semibold text-gray-800 transition-colors"
                    :class="{
                      'group-hover:text-purple-600': index === 0,
                      'group-hover:text-cyan-600': index === 1,
                      'group-hover:text-pink-600': index === 2
                    }"
                  >{{ announcement.title }}</h4>
                  <span class="text-xs text-gray-500 whitespace-nowrap ml-2">{{ formatTime(announcement.created_at) }}</span>
                </div>
                <p class="text-sm text-gray-600 mb-2">{{ announcement.content }}</p>
                <div class="text-xs text-gray-400">发布者：{{ announcement.author_real_name || announcement.author_name }}</div>
              </div>
              
              <!-- 如果没有公告，显示提示 -->
              <div v-if="announcements.length === 0" class="text-center py-8 text-gray-400">
                暂无公告
              </div>
            </div>
          </div>

          <!-- Quick Stats & Reminders -->
          <div class="space-y-6">
            <!-- Stats Card -->
            <div class="bg-white rounded-2xl p-8 shadow-lg border border-cyan-100">
              <div class="flex items-center mb-6">
                <div class="w-12 h-12 bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-xl flex items-center justify-center mr-4">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                  </svg>
                </div>
                <h3 class="text-2xl font-bold text-gray-800">实时数据</h3>
              </div>
              
              <div class="grid grid-cols-2 gap-4">
                <div class="p-4 rounded-xl bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200">
                  <div class="text-3xl font-black gradient-text-large mb-1">12</div>
                  <div class="text-sm text-gray-600">待审核工单</div>
                </div>
                <div class="p-4 rounded-xl bg-gradient-to-br from-cyan-50 to-cyan-100 border border-cyan-200">
                  <div class="text-3xl font-black gradient-text-large mb-1">8</div>
                  <div class="text-sm text-gray-600">维修中</div>
                </div>
                <div class="p-4 rounded-xl bg-gradient-to-br from-pink-50 to-pink-100 border border-pink-200">
                  <div class="text-3xl font-black gradient-text-large mb-1">25</div>
                  <div class="text-sm text-gray-600">今日完成</div>
                </div>
                <div class="p-4 rounded-xl bg-gradient-to-br from-indigo-50 to-indigo-100 border border-indigo-200">
                  <div class="text-3xl font-black gradient-text-large mb-1">5</div>
                  <div class="text-sm text-gray-600">待接单</div>
                </div>
              </div>
            </div>

            <!-- Important Reminders -->
            <div class="bg-white rounded-2xl p-8 shadow-lg border border-pink-100">
              <div class="flex items-center mb-6">
                <div class="w-12 h-12 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center mr-4">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <h3 class="text-2xl font-bold text-gray-800">重要提醒</h3>
              </div>
              
              <div class="space-y-3">
                <div class="flex items-center p-3 rounded-lg bg-yellow-50 border border-yellow-200">
                  <div class="w-2 h-2 bg-yellow-500 rounded-full mr-3 animate-pulse"></div>
                  <span class="text-sm text-gray-700">紧急工单需在2小时内响应</span>
                </div>
                <div class="flex items-center p-3 rounded-lg bg-blue-50 border border-blue-200">
                  <div class="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                  <span class="text-sm text-gray-700">定期检查工单处理进度</span>
                </div>
                <div class="flex items-center p-3 rounded-lg bg-green-50 border border-green-200">
                  <div class="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                  <span class="text-sm text-gray-700">及时更新维修状态信息</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section - Full Width -->
    <section id="features" class="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-purple-50 via-white to-cyan-50">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl sm:text-5xl font-bold mb-4">
            <span class="gradient-text-large">核心功能</span>
          </h2>
          <p class="text-xl text-gray-600">完整的工单流转系统，满足各角色需求</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Feature Card 1 -->
          <div class="group relative bg-gradient-to-br from-purple-50 to-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 cursor-pointer border border-purple-100">
            <div class="absolute top-0 right-0 w-32 h-32 bg-purple-200 rounded-full filter blur-3xl opacity-0 group-hover:opacity-50 transition-opacity duration-300"></div>
            <div class="relative">
              <div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mb-4 shadow-lg">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-800 mb-3">学生端</h3>
              <ul class="space-y-2 text-gray-600">
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  在线提交报修申请
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  实时跟踪工单状态
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  上传现场照片
                </li>
              </ul>
            </div>
          </div>

          <!-- Feature Card 2 -->
          <div class="group relative bg-gradient-to-br from-cyan-50 to-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 cursor-pointer border border-cyan-100">
            <div class="absolute top-0 right-0 w-32 h-32 bg-cyan-200 rounded-full filter blur-3xl opacity-0 group-hover:opacity-50 transition-opacity duration-300"></div>
            <div class="relative">
              <div class="w-14 h-14 bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-xl flex items-center justify-center mb-4 shadow-lg">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-800 mb-3">管理员端</h3>
              <ul class="space-y-2 text-gray-600">
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  数据可视化仪表盘
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  智能派单系统
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  工单审核管理
                </li>
              </ul>
            </div>
          </div>

          <!-- Feature Card 3 -->
          <div class="group relative bg-gradient-to-br from-pink-50 to-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 cursor-pointer border border-pink-100">
            <div class="absolute top-0 right-0 w-32 h-32 bg-pink-200 rounded-full filter blur-3xl opacity-0 group-hover:opacity-50 transition-opacity duration-300"></div>
            <div class="relative">
              <div class="w-14 h-14 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center mb-4 shadow-lg">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-800 mb-3">维修员端</h3>
              <ul class="space-y-2 text-gray-600">
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  接收派单通知
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  更新维修进度
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  查看工单详情
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-12 px-4 sm:px-6 lg:px-8 bg-white border-t border-gray-200">
      <div class="max-w-7xl mx-auto text-center">
        <p class="text-lg font-medium text-gray-800 mb-2">DormFix - 基于 Django 的宿舍报修工单系统</p>
        <p class="text-sm text-gray-600">毕业设计项目 © 2026</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getLatestAnnouncements } from '@/api'

const announcements = ref([])

const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  }
};

// 获取最新公告
const fetchAnnouncements = async () => {
  try {
    const { data } = await getLatestAnnouncements()
    announcements.value = data
  } catch (error) {
    console.error('获取公告失败:', error)
    // 如果获取失败，使用默认公告
    announcements.value = [
      {
        id: 1,
        title: '系统维护通知',
        content: '系统将于本周六凌晨2:00-4:00进行例行维护，期间可能无法访问。',
        author_real_name: '系统管理员',
        created_at: '2小时前'
      },
      {
        id: 2,
        title: '新功能上线',
        content: '工单审核流程已优化，管理员可以更高效地处理报修申请。',
        author_real_name: '系统管理员',
        created_at: '1天前'
      },
      {
        id: 3,
        title: '服务时间调整',
        content: '维修服务时间调整为工作日 8:00-18:00，节假日暂停服务。',
        author_real_name: '系统管理员',
        created_at: '3天前'
      }
    ]
  }
}

// 格式化时间
const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000) // 秒
  
  if (diff < 60) return '刚刚'
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`
  if (diff < 2592000) return `${Math.floor(diff / 86400)}天前`
  
  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  fetchAnnouncements()
})
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(135deg, #7C3AED 0%, #22D3EE 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.gradient-text-large {
  background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 50%, #22D3EE 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
}

@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes blob {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes fade-in-down {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-in-up {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-down {
  animation: fade-in-down 0.6s ease-out;
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out;
}

.animation-delay-200 {
  animation-delay: 0.2s;
  opacity: 0;
  animation-fill-mode: forwards;
}

.animation-delay-400 {
  animation-delay: 0.4s;
  opacity: 0;
  animation-fill-mode: forwards;
}

.animation-delay-600 {
  animation-delay: 0.6s;
  opacity: 0;
  animation-fill-mode: forwards;
}

.animation-delay-800 {
  animation-delay: 0.8s;
  opacity: 0;
  animation-fill-mode: forwards;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-5px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

.animate-float:nth-child(1) {
  animation-delay: 0s;
}

.animate-float:nth-child(2) {
  animation-delay: 0.2s;
}

.animate-float:nth-child(3) {
  animation-delay: 0.4s;
}

.animate-float:nth-child(4) {
  animation-delay: 0.6s;
}
</style>
