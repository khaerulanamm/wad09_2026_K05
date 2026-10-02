const API_BASE_URL = "http://localhost:8000"

export class ApiError extends Error {
  constructor(message, status, detail) {
    super(message)
    this.name = "ApiError"
    this.status = status
    this.detail = detail
  }
}

// Dipakai oleh api-write.js (Bagian D) untuk POST/DELETE.
export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options)

  if (response.status === 204) return null

  const body = await response.json().catch(() => null)

  if (!response.ok) {
    const detail = body?.detail
    const message = typeof detail === "string" ? detail : "Terjadi kesalahan pada server."
    throw new ApiError(message, response.status, detail)
  }

  return body
}

export async function fetchSessions({
  skip = 0,
  limit = 10,
  search = "",
  signal,
} = {}) {
  const params = new URLSearchParams({
    skip: String(skip),
    limit: String(limit),
  })

  if (search.trim()) {
    params.set("search", search.trim())
  }

  const response = await fetch(
    `${API_BASE_URL}/sessions?${params.toString()}`,
    { signal }
  )

  if (!response.ok) {
    throw new Error(`Gagal mengambil sesi (${response.status})`)
  }

  return response.json()
}

export async function fetchSession(id, signal) {
  const response = await fetch(
    `${API_BASE_URL}/sessions/${id}`,
    { signal }
  )

  if (!response.ok) {
    throw new Error(`Gagal mengambil sesi (${response.status})`)
  }

  return response.json()
}