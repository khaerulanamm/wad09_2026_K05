<script setup>
import { nextTick, ref } from 'vue'
import { deleteSession } from '../api-write.js'

const props = defineProps({ session: { type: Object, required: true } })
const emit = defineEmits(['deleted'])

const confirming = ref(false)
const busy = ref(false)
const error = ref('')
const confirmButton = ref(null)
const askButton = ref(null)

// F4: hapus dua langkah. Klik "Hapus", lalu konfirmasi "Ya, hapus".
async function ask() {
  error.value = ''
  confirming.value = true
  await nextTick()
  confirmButton.value?.focus()
}

async function cancel() {
  confirming.value = false
  await nextTick()
  askButton.value?.focus()
}

async function remove() {
  busy.value = true
  try {
    await deleteSession(props.session.id)
    emit('deleted')
  } catch (err) {
    error.value = err.message
    if (err.status === 404) emit('deleted') // sudah terhapus di tempat lain: tetap segarkan daftar
  } finally {
    busy.value = false
    confirming.value = false
  }
}
</script>

<template>
  <div class="delete">
    <button v-if="!confirming" ref="askButton" type="button" class="btn-secondary" @click="ask">
      Hapus
    </button>
    <div v-else class="row" role="group" :aria-label="`Konfirmasi hapus ${session.class_name}`">
      <span>Hapus kelas "{{ session.class_name }}"?</span>
      <button ref="confirmButton" type="button" class="btn-danger" :disabled="busy" @click="remove">
        Ya, hapus
      </button>
      <button type="button" class="btn-secondary" :disabled="busy" @click="cancel">Batal</button>
    </div>
    <p v-if="error" class="field-error" role="alert">{{ error }}</p>
  </div>
</template>
