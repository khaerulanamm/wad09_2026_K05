<script setup>
import { computed } from 'vue'
import { PAGE_SIZE, useSessions } from '../composables/useSessions.js'
import PagerNav from './PagerNav.vue'
import SearchBar from './SearchBar.vue'
import SessionCard from './SessionCard.vue'

const { status, items, total, error, page, search, load } = useSessions()
const pageCount = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)))
const keyword = computed(() => search.value.trim())

function onSearch() {
  page.value = 0
  load()
}

function goTo(newPage) {
  page.value = newPage
  load()
}

// Dipanggil App.vue setelah sesi ditambah atau dihapus.
defineExpose({ reload: load })
</script>

<template>
  <section class="panel" aria-labelledby="list-title">
    <h2 id="list-title">Jadwal kelas</h2>
    <SearchBar v-model="search" @search="onSearch" />

    <p v-if="status === 'loading'" class="notice" role="status">Memuat jadwal…</p>

    <div v-else-if="status === 'error'" class="notice notice-error" role="alert">
      <p>{{ error }}</p>
      <button type="button" @click="load">Coba lagi</button>
    </div>

    <p v-else-if="status === 'empty'" class="notice" role="status">
      <template v-if="keyword">Tidak ada kelas yang cocok dengan "{{ keyword }}".</template>
      <template v-else>Belum ada jadwal kelas. Tambahkan lewat form.</template>
    </p>

    <template v-else>
      <p class="muted">{{ total }} kelas ditemukan</p>
      <ul class="session-list">
        <li v-for="session in items" :key="session.id">
          <SessionCard :session="session">
            <slot name="actions" :session="session" />
          </SessionCard>
        </li>
      </ul>
      <PagerNav :page="page" :page-count="pageCount" @change="goTo" />
    </template>
  </section>
</template>
