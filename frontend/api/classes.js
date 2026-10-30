import { apiRequest } from './client.js'

export function listClasses({ skip = 0, limit = 10, search = '' } = {}, signal) {
  const params = new URLSearchParams({ skip, limit })
  if (search.trim()) params.set('search', search.trim())
  return apiRequest(`/classes?${params}`, { signal })
}

export const createClass = (data) => apiRequest('/classes', { method: 'POST', body: JSON.stringify(data) })
export const updateClass = (id, data) => apiRequest(`/classes/${id}`, { method: 'PATCH', body: JSON.stringify(data) })
export const deleteClass = (id) => apiRequest(`/classes/${id}`, { method: 'DELETE' })
