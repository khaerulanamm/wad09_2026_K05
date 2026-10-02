import { onMounted, onUnmounted, ref } from 'vue'
import { listSessions } from '../api.js'

export const PAGE_SIZE = 5

// F1 + F2: mengambil daftar saat mount, membatalkan permintaan saat unmount,
// dan menyimpan satu dari empat state: 'loading' | 'data' | 'empty' | 'error'.
export function useSessions() {
  const status = ref('loading')
  const items = ref([])
  const total = ref(0)
  const error = ref('')
  const page = ref(0)
  const search = ref('')
  let controller = null

  async function load() {
    controller?.abort() // permintaan lama dibatalkan supaya hasilnya tidak menimpa yang baru
    controller = new AbortController()
    status.value = 'loading'
    try {
      const query = { skip: page.value * PAGE_SIZE, limit: PAGE_SIZE, search: search.value.trim() }
      const data = await listSessions(query, controller.signal)
      // Halaman terakhir bisa kosong setelah item terakhirnya dihapus: mundur satu halaman.
      if (data.items.length === 0 && data.total > 0 && page.value > 0) {
        page.value -= 1
        return load()
      }
      items.value = data.items
      total.value = data.total
      status.value = data.items.length ? 'data' : 'empty'
    } catch (err) {
      if (err.name === 'AbortError') return
      error.value = err.message
      status.value = 'error'
    }
  }

  onMounted(load)
  onUnmounted(() => controller?.abort())

  return { status, items, total, error, page, search, load }
}
