import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { api } from './api'
import { useUserStore } from './stores/user'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err.response?.status === 401) {
      useUserStore().setUser(null)
      const to = window.location.pathname
      if (!to.startsWith('/login') && !to.startsWith('/register')) {
        router.push({ name: 'Login', query: { redirect: to } })
      }
    }
    return Promise.reject(err)
  }
)

app.mount('#app')
