<template>
  <div class="app">
    <header class="app-header">
      <div class="container header-content">
        <div>
          <p class="eyebrow">FITNESS CENTER</p>
          <h1>Jadwal Kelas Gym</h1>
          <p class="subtitle">Temukan jadwal kelas dan instruktur yang sesuai dengan kebutuhanmu.</p>
        </div>
        <nav class="auth-nav" aria-label="Akun">
          <template v-if="currentUser">
            <span>{{ currentUser.name }} · {{ currentUser.role }}</span>
            <button v-if="currentUser.role === 'admin'" type="button" class="btn-secondary" @click="authPanel = 'register'">Tambah akun</button>
            <button type="button" class="btn-secondary" @click="showProfile = !showProfile">Profil saya</button>
            <button type="button" class="btn-secondary" @click="signOut">Keluar</button>
          </template>
          <button v-else type="button" class="btn-secondary" @click="authPanel = 'login'">Masuk</button>
        </nav>
      </div>
    </header>

    <main class="container">
      <section v-if="authPanel === 'login'" class="auth-wrap">
        <LoginForm @done="authDone" />
        <button type="button" class="plain-button" @click="authPanel = ''">Tutup</button>
      </section>
      <section v-else-if="authPanel === 'register' && currentUser?.role === 'admin'" class="auth-wrap">
        <RegisterForm />
        <button type="button" class="plain-button" @click="authPanel = ''">Tutup</button>
      </section>

      <ProfileForm v-if="currentUser && showProfile" :user="currentUser" />
      <ClassForm v-if="currentUser" :editing-class="classEditing" @saved="classSaved" @cancel="classEditing = null" />

      <section class="search-section" aria-labelledby="search-title">
        <h2 id="search-title">Cari Kelas</h2>
        <SearchBar :initial-value="search" @search="setSearch" />
      </section>

      <ClassList
        :classes="classes"
        :total="total"
        :status="status"
        :error="error"
        :user="currentUser"
        @retry="retry"
        @deleted="retry"
        @edit="classEditing = $event"
      />
      <Pagination
        :skip="page * PAGE_SIZE"
        :limit="PAGE_SIZE"
        :total="total"
        :loading="status === 'loading'"
        @previous="goTo(page - 1)"
        @next="goTo(page + 1)"
      />
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAuth } from './composables/useAuth.js'
import { PAGE_SIZE, useClasses } from './composables/useClasses.js'
import LoginForm from './components/auth/LoginForm.vue'
import ProfileForm from './components/auth/ProfileForm.vue'
import RegisterForm from './components/auth/RegisterForm.vue'
import Pagination from './components/Pagination.vue'
import SearchBar from './components/SearchBar.vue'
import ClassForm from './components/ClassForm.vue'
import ClassList from './components/ClassList.vue'

const { currentUser, initialize, logout } = useAuth()
const { items: classes, total, page, search, status, error, retry, setSearch, goTo } = useClasses()
const authPanel = ref('')
const showProfile = ref(false)
const classEditing = ref(null)

onMounted(initialize)

function authDone() {
  authPanel.value = ''
  showProfile.value = false
  retry()
}

function signOut() {
  logout()
  authPanel.value = ''
  showProfile.value = false
  classEditing.value = null
}

function classSaved() {
  classEditing.value = null
  retry()
}
</script>
