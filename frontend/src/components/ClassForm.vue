<script setup>
import { nextTick, reactive, ref, watch } from 'vue'
import { createClass, updateClass } from '../api/classes.js'
import { LEVELS, emptyClass, serverFieldErrors, validateClass } from '../validate.js'
import FormField from './FormField.vue'

const props = defineProps({ editingClass: { type: Object, default: null } })
const emit = defineEmits(['saved', 'cancel'])
const form = reactive(emptyClass())
const errors = ref({})
const serverError = ref('')
const success = ref('')
const saving = ref(false)

watch(() => props.editingClass, (item) => {
  Object.assign(form, item ? {
    class_name: item.class_name,
    instructor: item.instructor,
    date: item.date,
    start_time: String(item.start_time).slice(0, 5),
    duration_min: item.duration_min,
    capacity: item.capacity,
    level: item.level,
  } : emptyClass())
  errors.value = {}
  serverError.value = ''
  success.value = ''
}, { immediate: true })

async function focusFirstError() {
  await nextTick()
  const first = Object.keys(errors.value)[0]
  if (first) document.getElementById(`f-${first}`)?.focus()
}

async function submit() {
  serverError.value = ''
  success.value = ''
  errors.value = validateClass(form)
  if (Object.keys(errors.value).length) return focusFirstError()

  saving.value = true
  try {
    const payload = { ...form }
    if (props.editingClass) await updateClass(props.editingClass.id, payload)
    else await createClass(payload)
    success.value = props.editingClass ? 'Jadwal berhasil diubah.' : `Kelas "${form.class_name}" berhasil ditambahkan.`
    if (!props.editingClass) Object.assign(form, emptyClass())
    emit('saved')
  } catch (err) {
    errors.value = serverFieldErrors(err)
    serverError.value = err.message
    focusFirstError()
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <section class="panel" aria-labelledby="form-title">
    <h2 id="form-title">{{ editingClass ? 'Ubah jadwal kelas' : 'Tambah jadwal kelas' }}</h2>
    <form novalidate @submit.prevent="submit">
      <FormField id="f-class_name" label="Nama kelas" :error="errors.class_name" v-slot="a">
        <input id="f-class_name" v-model="form.class_name" maxlength="60" :aria-invalid="a.invalid" :aria-describedby="a.describedby" />
      </FormField>
      <FormField id="f-instructor" label="Instruktur" :error="errors.instructor" v-slot="a">
        <input id="f-instructor" v-model="form.instructor" maxlength="60" :aria-invalid="a.invalid" :aria-describedby="a.describedby" />
      </FormField>
      <FormField id="f-date" label="Tanggal" :error="errors.date" v-slot="a">
        <input id="f-date" v-model="form.date" type="date" :aria-invalid="a.invalid" :aria-describedby="a.describedby" />
      </FormField>
      <FormField id="f-start_time" label="Jam mulai" :error="errors.start_time" v-slot="a">
        <input id="f-start_time" v-model="form.start_time" type="time" :aria-invalid="a.invalid" :aria-describedby="a.describedby" />
      </FormField>
      <FormField id="f-duration_min" label="Durasi (menit)" :error="errors.duration_min" v-slot="a">
        <input id="f-duration_min" v-model.number="form.duration_min" type="number" min="15" max="180" :aria-invalid="a.invalid" :aria-describedby="a.describedby" />
      </FormField>
      <FormField id="f-capacity" label="Kapasitas (orang)" :error="errors.capacity" v-slot="a">
        <input id="f-capacity" v-model.number="form.capacity" type="number" min="1" max="50" :aria-invalid="a.invalid" :aria-describedby="a.describedby" />
      </FormField>
      <FormField id="f-level" label="Level" :error="errors.level" v-slot="a">
        <select id="f-level" v-model="form.level" :aria-invalid="a.invalid" :aria-describedby="a.describedby">
          <option v-for="level in LEVELS" :key="level.value" :value="level.value">{{ level.label }}</option>
        </select>
      </FormField>
      <p v-if="serverError" class="notice notice-error" role="alert">{{ serverError }}</p>
      <p v-if="success" class="notice notice-success" role="status">{{ success }}</p>
      <div class="row">
        <button type="submit" :disabled="saving">{{ saving ? 'Menyimpan…' : 'Simpan' }}</button>
        <button v-if="editingClass" type="button" class="btn-secondary" @click="emit('cancel')">Batal</button>
      </div>
    </form>
  </section>
</template>
