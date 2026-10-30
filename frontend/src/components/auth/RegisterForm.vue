<script setup>
import { reactive, ref } from 'vue'
import { useAuth } from '../../composables/useAuth.js'
import FormField from '../FormField.vue'

const { createUser } = useAuth()
const form = reactive({ name: '', email: '', password: '' })
const error = ref('')
const success = ref('')
const saving = ref(false)

async function submit() {
  saving.value = true
  error.value = ''
  success.value = ''
  try {
    const user = await createUser({ ...form })
    success.value = `Akun ${user.name} (${user.email}) berhasil dibuat.`
    form.name = ''
    form.email = ''
    form.password = ''
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <section class="panel auth-panel" aria-labelledby="register-title">
    <h2 id="register-title">Tambah akun user</h2>
    <form @submit.prevent="submit">
      <FormField id="register-name" label="Nama">
        <input id="register-name" v-model="form.name" maxlength="80" autocomplete="name" required />
      </FormField>
      <FormField id="register-email" label="Email">
        <input id="register-email" v-model="form.email" type="email" autocomplete="email" required />
      </FormField>
      <FormField id="register-password" label="Password">
        <input id="register-password" v-model="form.password" type="password" minlength="8" maxlength="72" autocomplete="new-password" required />
      </FormField>
      <p v-if="error" class="notice notice-error" role="alert">{{ error }}</p>
      <p v-if="success" class="notice notice-success" role="status">{{ success }}</p>
      <div class="row">
        <button type="submit" :disabled="saving">{{ saving ? 'Menyimpan…' : 'Buat akun' }}</button>
      </div>
    </form>
  </section>
</template>
