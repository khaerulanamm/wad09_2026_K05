import { computed, ref } from 'vue'
import { getMe, login as loginRequest, register as registerRequest, updateUser } from '../api/auth.js'
import { getAccessToken, setAccessToken } from '../api/client.js'

const token = ref(getAccessToken())
const currentUser = ref(null)
const initialized = ref(false)

export function useAuth() {
  const isAuthenticated = computed(() => Boolean(currentUser.value))
  const isAdmin = computed(() => currentUser.value?.role === 'admin')

  async function login(credentials) {
    const result = await loginRequest(credentials)
    setAccessToken(result.access_token)
    token.value = result.access_token
    currentUser.value = await getMe()
    return currentUser.value
  }

  async function createUser(data) {
    return registerRequest(data)
  }

  async function updateProfile(data) {
    const updated = await updateUser(currentUser.value.id, data)
    currentUser.value = updated
    return updated
  }

  function logout() {
    setAccessToken('')
    token.value = ''
    currentUser.value = null
  }

  async function initialize() {
    if (initialized.value) return
    initialized.value = true
    if (!token.value) return
    try {
      currentUser.value = await getMe()
    } catch {
      logout()
    }
  }

  return { token, currentUser, initialized, isAuthenticated, isAdmin, login, createUser, updateProfile, logout, initialize }
}
