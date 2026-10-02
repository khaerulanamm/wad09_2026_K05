<script setup>
const search = defineModel({ type: String, default: '' })
const emit = defineEmits(['search'])
</script>

<template>
  <form class="search" role="search" @submit.prevent="emit('search')">
    <label for="search-input">Cari kelas atau instruktur</label>
    <div class="row">
      <input id="search-input" v-model="search" type="search" maxlength="50" placeholder="mis. yoga" />
      <button type="submit">Cari</button>
    </div>
  </form>
</template>
