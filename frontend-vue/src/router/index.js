import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/HomeView.vue'), meta: { hideNav: false } },
  { path: '/login', name: 'Login', component: () => import('@/views/LoginView.vue'), meta: { hideNav: true } },
  { path: '/register', name: 'Register', component: () => import('@/views/RegisterView.vue'), meta: { hideNav: true } },
  { 
    path: '/submit', 
    name: 'SubmitOrder', 
    component: () => import('@/views/SubmitOrderView.vue'),
    meta: { requiresAuth: true, roles: [1] } // 仅学生可访问
  },
  { 
    path: '/orders', 
    name: 'OrderTracking', 
    component: () => import('@/views/OrderTrackingView.vue'),
    meta: { requiresAuth: true, roles: [1, 2, 3] } // 所有角色可访问
  },
  { 
    path: '/admin', 
    name: 'AdminDashboard', 
    component: () => import('@/views/AdminDashboardView.vue'),
    meta: { requiresAuth: true, roles: [3] } // 仅管理员可访问
  },
  { 
    path: '/admin/users', 
    name: 'UserManagement', 
    component: () => import('@/views/UserManagementView.vue'),
    meta: { requiresAuth: true, roles: [3] } // 仅管理员可访问
  },
  { 
    path: '/admin/logs', 
    name: 'OperationLogs', 
    component: () => import('@/views/OperationLogsView.vue'),
    meta: { requiresAuth: true, roles: [3] } // 仅管理员可访问
  },
  { 
    path: '/admin/review', 
    name: 'AdminReview', 
    component: () => import('@/views/AdminReviewView.vue'),
    meta: { requiresAuth: true, roles: [3] } // 仅管理员可访问
  },
  { 
    path: '/repairman/accept', 
    name: 'RepairmanAccept', 
    component: () => import('@/views/RepairmanAcceptView.vue'),
    meta: { requiresAuth: true, roles: [2] } // 仅维修人员可访问
  },
  { 
    path: '/repairman/orders', 
    name: 'RepairmanOrders', 
    component: () => import('@/views/RepairmanOrdersView.vue'),
    meta: { requiresAuth: true, roles: [2] } // 仅维修人员可访问
  },
  { 
    path: '/profile', 
    name: 'Profile', 
    component: () => import('@/views/ProfileView.vue'),
    meta: { requiresAuth: true, roles: [1, 2, 3] } // 所有角色可访问
  },
  { 
    path: '/settings', 
    name: 'Settings', 
    component: () => import('@/views/SettingsView.vue'),
    meta: { requiresAuth: true, roles: [1, 2, 3] } // 所有角色可访问
  },
  { path: '/debug', name: 'Debug', component: () => import('@/views/DebugView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (!userStore.isLoggedIn) {
      // 未登录，重定向到登录页
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
    
    // 检查角色权限
    if (to.meta.roles && to.meta.roles.length > 0) {
      const userRole = userStore.user?.role
      if (!to.meta.roles.includes(userRole)) {
        // 权限不足，重定向到首页
        alert('您没有权限访问该页面')
        next({ name: 'Home' })
        return
      }
    }
  }
  
  // 已登录用户访问登录/注册页，重定向到首页
  if ((to.name === 'Login' || to.name === 'Register') && userStore.isLoggedIn) {
    next({ name: 'Home' })
    return
  }
  
  next()
})

export default router
