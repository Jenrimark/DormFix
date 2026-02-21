import axios from 'axios'

export const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
  // Django CSRF：从 cookie 读 csrftoken，POST 时自动带 X-CSRFToken 头，避免 403
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
})

// 响应拦截器 - 全局错误处理
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const status = error.response.status
      const message = error.response.data?.error || error.response.data?.detail || '操作失败'
      
      switch (status) {
        case 401:
          // 未认证 - 清除用户状态并重定向到登录页
          console.error('未认证，请重新登录')
          // 使用 window.location 而不是 router，因为这里无法访问 router
          if (!window.location.pathname.includes('/login')) {
            window.location.href = '/login'
          }
          break
        case 403:
          // 权限不足
          console.error('权限不足:', message)
          alert('权限不足：' + message)
          break
        case 404:
          // 资源不存在
          console.error('资源不存在:', message)
          break
        case 500:
          // 服务器错误
          console.error('服务器错误:', message)
          alert('服务器错误，请稍后重试')
          break
        default:
          console.error('请求错误:', message)
      }
    } else if (error.request) {
      // 请求已发送但没有收到响应
      console.error('网络错误，请检查网络连接')
      alert('网络错误，请检查网络连接')
    } else {
      // 请求配置出错
      console.error('请求配置错误:', error.message)
    }
    
    return Promise.reject(error)
  }
)

// 用户
export const login = (data) => api.post('/accounts/users/login/', data)
export const logout = () => api.post('/accounts/users/logout/')
export const register = (data) => api.post('/accounts/users/register/', data)
export const getMe = () => api.get('/accounts/users/me/')
export const updateProfile = (data) => api.put('/accounts/users/update_profile/', data)
export const uploadAvatar = (formData) => api.post('/accounts/users/upload_avatar/', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
export const changePassword = (data) => api.put('/accounts/users/change_password/', data)

// 故障类型
export const getRepairTypes = () => api.get('/repairs/repair-types/')

// 工单
export const getWorkOrders = (params) => api.get('/repairs/work-orders/', { params })
export const getMyOrders = (params) => api.get('/repairs/work-orders/my_orders/', { params })
export const getPendingOrders = () => api.get('/repairs/work-orders/pending/')
export const createWorkOrder = (data) => {
  // 如果是 FormData，自动设置正确的 Content-Type
  const config = data instanceof FormData ? {
    headers: { 'Content-Type': 'multipart/form-data' }
  } : {}
  return api.post('/repairs/work-orders/', data, config)
}
export const assignOrder = (id, repairmanId) => api.post(`/repairs/work-orders/${id}/assign/`, { repairman_id: repairmanId })
export const updateOrderStatus = (id, status, remark) => api.post(`/repairs/work-orders/${id}/update_status/`, { status, remark })
export const getStatistics = () => api.get('/repairs/work-orders/statistics/')
export const getTypeDistribution = () => api.get('/repairs/work-orders/type_distribution/')

// 评价
export const createComment = (data) => api.post('/repairs/comments/', data)

// 用户管理（管理员）
export const listAllUsers = (params) => api.get('/accounts/users/list_all/', { params })
export const createUser = (data) => api.post('/accounts/users/create_user/', data)
export const updateUser = (id, data) => api.put(`/accounts/users/${id}/update_user/`, data)
export const deleteUser = (id) => api.delete(`/accounts/users/${id}/delete_user/`)
export const resetPassword = (id) => api.post(`/accounts/users/${id}/reset_password/`)
export const toggleUserStatus = (id) => api.post(`/accounts/users/${id}/toggle_status/`)
export const batchOperation = (data) => api.post('/accounts/users/batch_operation/', data)

// 操作日志（管理员）
export const getOperationLogs = (params) => api.get('/accounts/operation-logs/', { params })

// 报修流程相关接口
export const reviewOrder = (id, data) => api.post(`/repairs/work-orders/${id}/review/`, data)
export const getAvailableOrders = (params) => api.get('/repairs/work-orders/available/', { params })
export const acceptOrder = (id) => api.post(`/repairs/work-orders/${id}/accept/`)
export const startRepair = (id) => api.post(`/repairs/work-orders/${id}/start_repair/`)
export const completeRepair = (id, formData) => api.post(`/repairs/work-orders/${id}/complete_repair/`, formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
