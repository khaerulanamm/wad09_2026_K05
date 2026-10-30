<script setup>
import { reactive, ref, watch } from 'vue'
import { useAuth } from '../../composables/useAuth.js'
import FormField from '../FormField.vue'

const props = defineProps({ user: { type: Object, required: true } })
const { updateProfile } = useAuth()
const form = reactive({ name: props.user.name, email: props.user.email })
const error = ref('')
const success = ref('')
const saving = ref(false)

watch(() => props.user, (user) => {
  form.name = user.name
  form.email = user.email
})

async function submit() {
  saving.value = true
  error.value = ''
  success.value = ''
  try {
    await updateProfile({ ...form })
    success.value = 'Profil berhasil diperbarui.'
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <section class="panel auth-panel" aria-labelledby="profile-title">
    <h2 id="profile-title">Profil saya</h2>
    <form @submit.prevent="submit">
      <FormField id="profile-name" label="Nama">
        <input id="profile-name" v-model="form.name" maxlength="80" autocomplete="name" required />
      </FormField>
      <FormField id="profile-email" label="Email">
        <input id="profile-email" v-model="form.email" type="email" autocomplete="email" required />
      </FormField>
      <p v-if="error" class="notice notice-error" role="alert">{{ error }}</p>
      <p v-if="success" class="notice notice-success" role="status">{{ success }}</p>
      <button type="submit" :disabled="saving">{{ saving ? 'Menyimpan…' : 'Simpan profil' }}</button>
    </form>
  </section>
</template>
