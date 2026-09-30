<template>
  <div class="app">
    <header class="app-header">
      <div class="container">
        <p class="eyebrow">FITNESS CENTER</p>
        <h1>Jadwal Kelas Gym</h1>
        <p class="subtitle">
          Temukan jadwal kelas dan instruktur yang sesuai dengan kebutuhanmu.
        </p>
      </div>
    </header>

    <main class="container">
      <section class="search-section" aria-labelledby="search-title">
        <h2 id="search-title">Cari Kelas</h2>
        <SearchBar
          :initial-value="search"
          @search="setSearch"
        />
      </section>

      <SessionList
        :sessions="sessions"
        :total="total"
        :loading="loading"
        :error="error"
        @retry="retry"
      />

      <Pagination
        :skip="skip"
        :limit="limit"
        :total="total"
        :loading="loading"
        @previous="previousPage"
        @next="nextPage"
      />
    </main>
  </div>
</template>

<script setup>
import SearchBar from "./components/SearchBar.vue"
import SessionList from "./components/SessionList.vue"
import Pagination from "./components/Pagination.vue"
import { useSessions } from "./composables/useSessions"

const {
  sessions,
  total,
  skip,
  limit,
  search,
  loading,
  error,
  retry,
  setSearch,
  nextPage,
  previousPage,
} = useSessions()
</script>