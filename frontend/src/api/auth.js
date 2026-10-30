import { apiRequest } from './client.js'

export const register = (data) => apiRequest('/auth/register', { method: 'POST', body: JSON.stringify(data) })
export const login = (data) => apiRequest('/auth/login', { method: 'POST', body: JSON.stringify(data) })
export const getMe = () => apiRequest('/auth/me')
export const getUser = (id) => apiRequest(`/users/${id}`)
export const updateUser = (id, data) => apiRequest(`/users/${id}`, { method: 'PATCH', body: JSON.stringify(data) })
