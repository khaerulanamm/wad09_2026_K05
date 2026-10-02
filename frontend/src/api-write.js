import { request } from './api.js'

export function createSession(data) {
  return request('/sessions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}

export function deleteSession(id) {
  return request(`/sessions/${id}`, { method: 'DELETE' })
}
