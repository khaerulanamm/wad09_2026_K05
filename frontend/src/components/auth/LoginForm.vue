<script setup>
import { reactive, ref } from 'vue'
import { useAuth } from '../../composables/useAuth.js'
import FormField from '../FormField.vue'

const emit = defineEmits(['done'])
const { login } = useAuth()
const form = reactive({ email: '', password: '' })
const error = ref('')
const saving = ref(false)

async function submit() {
  saving.value = true
  error.value = ''
  try {
    await login({ ...form })
    emit('done')
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <section class="panel auth-panel" aria-labelledby="login-title">
    <h2 id="login-title">Masuk</h2>
    <form @submit.prevent="submit">
      <FormField id="login-email" label="Email">
        <input id="login-email" v-model="form.email" type="email" autocomplete="email" required />
      </FormField>
      <FormField id="login-password" label="Password">
        <input id="login-password" v-model="form.password" type="password" autocomplete="current-password" required />
      </FormField>
      <p v-if="error" class="notice notice-error" role="alert">{{ error }}</p>
      <div class="row">
        <button type="submit" :disabled="saving">{{ saving ? 'Memeriksa…' : 'Masuk' }}</button>
      </div>
    </form>
  </section>
</template>
