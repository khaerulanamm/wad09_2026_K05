<script setup>
defineProps({
  page: { type: Number, required: true },
  pageCount: { type: Number, required: true },
})
const emit = defineEmits(['change'])
</script>

<template>
  <nav class="pager" aria-label="Halaman jadwal">
    <button type="button" :disabled="page === 0" @click="emit('change', page - 1)">
      Sebelumnya
    </button>
    <span aria-live="polite">Halaman {{ page + 1 }} dari {{ pageCount }}</span>
    <button type="button" :disabled="page + 1 >= pageCount" @click="emit('change', page + 1)">
      Berikutnya
    </button>
  </nav>
</template>
