<template>
  <section class="session-list" aria-labelledby="session-list-title">
    <div class="section-heading">
      <h2 id="session-list-title">Daftar Kelas</h2>
      <span>{{ total }} sesi</span>
    </div>

    <div v-if="loading" class="state-message" role="status">
      Memuat jadwal kelas...
    </div>

    <div v-else-if="error" class="state-message state-error" role="alert">
      <p>{{ error }}</p>
      <button type="button" @click="$emit('retry')">
        Coba Lagi
      </button>
    </div>

    <div v-else-if="sessions.length === 0" class="state-message">
      Tidak ada kelas yang ditemukan.
    </div>

    <div v-else class="session-grid">
      <SessionCard
        v-for="session in sessions"
        :key="session.id"
        :session="session"
      />
    </div>
  </section>
</template>

<script setup>
import SessionCard from "./SessionCard.vue"

defineProps({
  sessions: {
    type: Array,
    required: true,
  },
  total: {
    type: Number,
    required: true,
  },
  loading: {
    type: Boolean,
    required: true,
  },
  error: {
    type: String,
    default: "",
  },
})

defineEmits(["retry"])
</script>