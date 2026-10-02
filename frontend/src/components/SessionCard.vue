<template>
  <article class="session-card">
    <div class="session-card__header">
      <h2>{{ session.class_name }}</h2>
      <span class="session-level">{{ session.level }}</span>
    </div>

    <p class="session-instructor">
      Instruktur: {{ session.instructor }}
    </p>

    <dl class="session-details">
      <div>
        <dt>Tanggal</dt>
        <dd>{{ session.date }}</dd>
      </div>

      <div>
        <dt>Mulai</dt>
        <dd>{{ session.start_time }}</dd>
      </div>

      <div>
        <dt>Durasi</dt>
        <dd>{{ session.duration_min }} menit</dd>
      </div>

      <div>
        <dt>Kapasitas</dt>
        <dd>{{ session.capacity }} peserta</dd>
      </div>
    </dl>

    <DeleteButton :session="session" @deleted="$emit('deleted')" />
  </article>
</template>

<script setup>
import DeleteButton from './DeleteButton.vue'

defineProps({
  session: {
    type: Object,
    required: true,
  },
})

defineEmits(['deleted'])
</script>