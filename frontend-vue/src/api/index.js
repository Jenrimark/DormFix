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
