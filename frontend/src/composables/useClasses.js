import { computed, onMounted, onUnmounted, ref } from 'vue'
import { listClasses } from '../api/classes.js'

export const PAGE_SIZE = 10

export function useClasses() {
  const items = ref([])
  const total = ref(0)
  const page = ref(0)
  const search = ref('')
  const status = ref('loading')
  const error = ref('')
  const pageCount = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)))
  let controller = null

  async function load() {
    controller?.abort()
    controller = new AbortController()
    status.value = 'loading'
    error.value = ''
    try {
      const result = await listClasses({
        skip: page.value * PAGE_SIZE,
        limit: PAGE_SIZE,
        search: search.value,
      }, controller.signal)
      if (!result.items.length && result.total > 0 && page.value > 0) {
        page.value -= 1
        return load()
      }
      items.value = result.items
      total.value = result.total
      status.value = result.items.length ? 'data' : 'empty'
    } catch (err) {
      if (err.name === 'AbortError') return
      error.value = err.message
      status.value = 'error'
    }
  }

  function retry() {
    load()
  }

  function setSearch(value) {
    search.value = value
    page.value = 0
    load()
  }

  function goTo(newPage) {
    if (newPage >= 0 && newPage < pageCount.value) {
      page.value = newPage
      load()
    }
  }

  onMounted(load)
  onUnmounted(() => controller?.abort())

  return { items, total, page, pageCount, search, status, error, retry, setSearch, goTo }
}
