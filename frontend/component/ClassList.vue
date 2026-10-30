<template>
  <section class="class-list" aria-labelledby="class-list-title">
    <div class="section-heading"><h2 id="class-list-title">Daftar Kelas</h2><span>{{ total }} kelas</span></div>
    <div v-if="status === 'loading'" class="state-message" role="status">Memuat jadwal kelas…</div>
    <div v-else-if="status === 'error'" class="state-message state-error" role="alert">
      <p>{{ error }}</p><button type="button" @click="$emit('retry')">Coba lagi</button>
    </div>
    <div v-else-if="status === 'empty'" class="state-message" role="status">Tidak ada kelas yang ditemukan.</div>
    <div v-else class="class-grid">
      <ClassCard
        v-for="classItem in classes"
        :key="classItem.id"
        :class-item="classItem"
        :user="user"
        @edit="$emit('edit', $event)"
        @deleted="$emit('deleted')"
      />
    </div>
  </section>
</template>

<script setup>
import ClassCard from './ClassCard.vue'

defineProps({
  classes: { type: Array, required: true },
  total: { type: Number, required: true },
  status: { type: String, required: true },
  error: { type: String, default: '' },
  user: { type: Object, default: null },
})
defineEmits(['retry', 'deleted', 'edit'])
</script>
