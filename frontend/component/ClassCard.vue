<template>
  <article class="class-card">
    <div class="class-card__header">
      <h2>{{ classItem.class_name }}</h2>
      <span class="class-level">{{ classItem.level }}</span>
    </div>
    <p class="class-instructor">Instruktur: {{ classItem.instructor }}</p>
    <dl class="class-details">
      <div><dt>Tanggal</dt><dd>{{ classItem.date }}</dd></div>
      <div><dt>Mulai</dt><dd>{{ classItem.start_time }}</dd></div>
      <div><dt>Durasi</dt><dd>{{ classItem.duration_min }} menit</dd></div>
      <div><dt>Kapasitas</dt><dd>{{ classItem.capacity }} peserta</dd></div>
    </dl>
    <div v-if="manageable" class="row class-actions">
      <button type="button" class="btn-secondary" @click="$emit('edit', classItem)">Ubah</button>
      <DeleteButton :class-item="classItem" @deleted="$emit('deleted')" />
    </div>
  </article>
</template>

<script setup>
import DeleteButton from './DeleteButton.vue'
import { computed } from 'vue'
import { canManage } from '../utils/permissions.js'

const props = defineProps({ classItem: { type: Object, required: true }, user: { type: Object, default: null } })
defineEmits(['edit', 'deleted'])
const manageable = computed(() => canManage(props.classItem.owner_id, props.user))
</script>
