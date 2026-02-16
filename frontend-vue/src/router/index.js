import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/HomeView.vue'), meta: { hideNav: false } },
  { path: '/login', name: 'Login', component: () => import('@/views/LoginView.vue'), meta: { hideNav: true } },
  { path: '/register', name: 'Register', component: () => import('@/views/RegisterView.vue'), meta: { hideNav: true } },
  { path: '/submit', name: 'SubmitOrder', component: () => import('@/views/SubmitOrderView.vue') },
  { path: '/orders', name: 'OrderTracking', component: () => import('@/views/OrderTrackingView.vue') },
  { path: '/admin', name: 'AdminDashboard', component: () => import('@/views/AdminDashboardView.vue') },
  { path: '/profile', name: 'Profile', component: () => import('@/views/ProfileView.vue') },
  { path: '/settings', name: 'Settings', component: () => import('@/views/SettingsView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
