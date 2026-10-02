const API_BASE_URL = "http://localhost:8000"

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