import { ref, onMounted, onUnmounted } from "vue"
import { fetchSessions } from "../api"

export function useSessions() {
  const sessions = ref([])
  const total = ref(0)
  const skip = ref(0)
  const limit = ref(10)
  const search = ref("")
  const loading = ref(false)
  const error = ref("")

  let controller = null

  async function loadSessions() {
    if (controller) {
      controller.abort()
    }

    controller = new AbortController()
    loading.value = true
    error.value = ""

    try {
      const result = await fetchSessions({
        skip: skip.value,
        limit: limit.value,
        search: search.value,
        signal: controller.signal,
      })

      sessions.value = result.items
      total.value = result.total
    } catch (err) {
      if (err.name !== "AbortError") {
        error.value = err.message
      }
    } finally {
      loading.value = false
    }
  }

  function retry() {
    loadSessions()
  }

  function setSearch(value) {
    search.value = value
    skip.value = 0
    loadSessions()
  }

  function nextPage() {
    if (skip.value + limit.value < total.value) {
      skip.value += limit.value
      loadSessions()
    }
  }

  function previousPage() {
    if (skip.value > 0) {
      skip.value = Math.max(0, skip.value - limit.value)
      loadSessions()
    }
  }

  onMounted(loadSessions)

  onUnmounted(() => {
    if (controller) {
      controller.abort()
    }
  })

  return {
    sessions,
    total,
    skip,
    limit,
    search,
    loading,
    error,
    retry,
    setSearch,
    nextPage,
    previousPage,
  }
}