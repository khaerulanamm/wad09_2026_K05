<template>
  <form class="search-form" @submit.prevent="submitSearch">
    <label for="session-search">Cari kelas atau instruktur</label>

    <div class="search-row">
      <input
        id="session-search"
        v-model="query"
        type="search"
        placeholder="Contoh: Yoga atau Rina"
      />
      <button type="submit">Cari</button>
    </div>
  </form>
</template>

<script setup>
import { ref } from "vue"

const props = defineProps({
  initialValue: {
    type: String,
    default: "",
  },
})

const emit = defineEmits(["search"])
const query = ref(props.initialValue)

function submitSearch() {
  emit("search", query.value)
}
</script>