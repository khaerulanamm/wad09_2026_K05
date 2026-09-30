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
  </article>
</template>

<script setup>
defineProps({
  session: {
    type: Object,
    required: true,
  },
})
</script>