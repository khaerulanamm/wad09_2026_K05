const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'
const TOKEN_KEY = 'gym_access_token'
let accessToken = localStorage.getItem(TOKEN_KEY) ?? ''

export function setAccessToken(token) {
  accessToken = token ?? ''
  if (accessToken) localStorage.setItem(TOKEN_KEY, accessToken)
  else localStorage.removeItem(TOKEN_KEY)
}

export function getAccessToken() {
  return accessToken
}

export class ApiError extends Error {
  constructor(status, detail) {
    super(typeof detail === 'string' ? detail : `Permintaan gagal (${status}).`)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

export async function apiRequest(path, options = {}) {
  const headers = new Headers(options.headers ?? {})
  if (accessToken) headers.set('Authorization', `Bearer ${accessToken}`)
  if (options.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json')

  let response
  try {
    response = await fetch(`${API_BASE}${path}`, { ...options, headers })
  } catch (error) {
    if (error.name === 'AbortError') throw error
    throw new ApiError(0, 'Server tidak dapat dihubungi. Pastikan backend berjalan.')
  }
  if (response.status === 204) return null
  const body = await response.json().catch(() => null)
  if (!response.ok) throw new ApiError(response.status, body?.detail ?? null)
  return body
}
