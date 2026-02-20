<template>
  <div>
    <!-- Hero Section -->
    <section class="text-center py-16">
      <span class="px-4 py-2 bg-primary/10 text-primary rounded-full text-sm font-medium">基于 Django + Vue3 的宿舍管理系统</span>
      <h1 class="font-heading text-4xl sm:text-5xl font-bold text-textDark mt-6 mb-4">让宿舍报修更简单、更高效</h1>
      <p class="text-lg text-gray-600 mb-10 max-w-2xl mx-auto">从报修到完工，全流程数字化管理。Vite 实时热更新，响应式界面。</p>
      <div class="flex flex-col sm:flex-row justify-center gap-4">
        <router-link to="/submit" class="px-8 py-4 bg-cta text-white rounded-lg font-medium hover:bg-cta/90 transition-all shadow-lg cursor-pointer">提交报修工单</router-link>
        <router-link to="/orders" class="px-8 py-4 bg-white text-gray-700 rounded-lg font-medium hover:bg-gray-50 border-2 border-gray-200 cursor-pointer">查看我的工单</router-link>
      </div>
      <div class="grid grid-cols-3 gap-8 mt-16 max-w-2xl mx-auto">
        <div><div class="font-heading text-3xl font-bold text-primary">2.3h</div><div class="text-gray-600 text-sm">平均响应</div></div>
        <div><div class="font-heading text-3xl font-bold text-primary">95%</div><div class="text-gray-600 text-sm">满意度</div></div>
        <div><div class="font-heading text-3xl font-bold text-primary">1000+</div><div class="text-gray-600 text-sm">处理工单</div></div>
      </div>
    </section>

    <!-- Core Features Section -->
    <section id="features" class="bg-white py-20">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="font-heading text-4xl font-bold text-textDark mb-4">核心功能</h2>
          <p class="text-xl text-gray-600">完整的工单流转系统，满足各角色需求</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Student Role Card -->
          <div class="bg-bgLight rounded-xl p-8 hover:shadow-lg transition-shadow duration-200 cursor-pointer">
            <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
            <h3 class="font-heading text-xl font-semibold text-textDark mb-3">学生端</h3>
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
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                评价维修服务
              </li>
            </ul>
          </div>

          <!-- Admin Role Card -->
          <div class="bg-bgLight rounded-xl p-8 hover:shadow-lg transition-shadow duration-200 cursor-pointer">
            <div class="w-12 h-12 bg-cta/10 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-cta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <h3 class="font-heading text-xl font-semibold text-textDark mb-3">管理员端</h3>
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
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                统计报表导出
              </li>
            </ul>
          </div>

          <!-- Technician Role Card -->
          <div class="bg-bgLight rounded-xl p-8 hover:shadow-lg transition-shadow duration-200 cursor-pointer">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <h3 class="font-heading text-xl font-semibold text-textDark mb-3">维修员端</h3>
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
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                填写维修备注
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Demo Section -->
    <section id="demo" class="py-20">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="font-heading text-4xl font-bold text-textDark mb-4">在线演示</h2>
          <p class="text-xl text-gray-600">快速体验系统各个功能模块</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <router-link to="/submit" class="bg-white rounded-xl p-6 border-2 border-gray-200 hover:border-primary hover:shadow-lg transition-all cursor-pointer">
            <div class="text-3xl mb-3">📝</div>
            <h3 class="font-heading text-lg font-semibold text-textDark">工单提交</h3>
            <p class="text-gray-600 text-sm">学生端 - 提交报修申请</p>
          </router-link>
          <router-link to="/admin" class="bg-white rounded-xl p-6 border-2 border-gray-200 hover:border-cta hover:shadow-lg transition-all cursor-pointer">
            <div class="text-3xl mb-3">📊</div>
            <h3 class="font-heading text-lg font-semibold text-textDark">管理仪表盘</h3>
            <p class="text-gray-600 text-sm">管理员 - 数据可视化</p>
          </router-link>
          <router-link to="/orders" class="bg-white rounded-xl p-6 border-2 border-gray-200 hover:border-blue-500 hover:shadow-lg transition-all cursor-pointer">
            <div class="text-3xl mb-3">🔍</div>
            <h3 class="font-heading text-lg font-semibold text-textDark">工单跟踪</h3>
            <p class="text-gray-600 text-sm">进度查询</p>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 py-8">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-600">
        <p class="text-lg font-medium mb-2">DormFix - 基于 Django 的宿舍报修工单系统</p>
        <p class="text-sm">软件工程专业毕业设计项目 © 2026</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>
