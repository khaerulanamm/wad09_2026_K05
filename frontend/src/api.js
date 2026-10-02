// Base URL dibaca dari environment, supaya tidak ada localhost yang tertulis mati di build produksi.
export const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

export class ApiError extends Error {
  constructor(status, detail) {
    super(typeof detail === 'string' ? detail : `Server menolak permintaan (${status}).`)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

// Satu pintu untuk semua fetch: error jaringan dan status non-2xx selalu jadi ApiError,
// sehingga pemanggil cukup satu try/catch dan tidak ada promise yang lolos tanpa ditangani.
export async function request(path, options = {}) {
  let res
  try {
    res = await fetch(`${API_BASE}${path}`, options)
  } catch (err) {
    if (err.name === 'AbortError') throw err
    throw new ApiError(0, 'Server tidak dapat dihubungi. Pastikan backend berjalan.')
  }
  if (res.status === 204) return null
  const body = await res.json().catch(() => null)
  if (!res.ok) throw new ApiError(res.status, body?.detail ?? null)
  return body
}

export function listSessions({ skip, limit, search }, signal) {
  const params = new URLSearchParams({ skip, limit })
  if (search) params.set('search', search)
  return request(`/sessions?${params}`, { signal })
}
