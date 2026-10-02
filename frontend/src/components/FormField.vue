<script setup>
// Pembungkus satu input: label, slot untuk input-nya, dan pesan error yang terhubung
// lewat aria-describedby supaya dibacakan pembaca layar.
defineProps({
  id: { type: String, required: true },
  label: { type: String, required: true },
  error: { type: String, default: '' },
})
</script>

<template>
  <div class="field">
    <label :for="id">{{ label }}</label>
    <slot :invalid="error ? 'true' : undefined" :describedby="error ? `${id}-error` : undefined" />
    <p v-if="error" :id="`${id}-error`" class="field-error">{{ error }}</p>
  </div>
</template>
