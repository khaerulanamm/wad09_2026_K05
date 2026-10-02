<script setup>
import { ref } from 'vue'
import DeleteButton from './components/DeleteButton.vue'
import SessionForm from './components/SessionForm.vue'
import SessionList from './components/SessionList.vue'

const list = ref(null)
const reload = () => list.value?.reload()
</script>

<template>
  <header class="site-header">
    <h1>Jadwal Kelas Gym</h1>
    <p>Catat dan kelola jadwal kelas fitness.</p>
  </header>
  <main class="layout">
    <SessionForm @created="reload" />
    <SessionList ref="list">
      <template #actions="{ session }">
        <DeleteButton :session="session" @deleted="reload" />
      </template>
    </SessionList>
  </main>
</template>
