<script setup>
defineProps({ session: { type: Object, required: true } })

const LEVELS = { beginner: 'Pemula', intermediate: 'Menengah', advanced: 'Lanjutan' }
</script>

<template>
  <article class="card">
    <h3>{{ session.class_name }}</h3>
    <dl>
      <dt>Instruktur</dt>
      <dd>{{ session.instructor }}</dd>
      <dt>Jadwal</dt>
      <dd>{{ session.date }}, {{ session.start_time }} ({{ session.duration_min }} menit)</dd>
      <dt>Kapasitas</dt>
      <dd>{{ session.capacity }} orang</dd>
      <dt>Level</dt>
      <dd>{{ LEVELS[session.level] ?? session.level }}</dd>
    </dl>
    <slot />
  </article>
</template>
