<template>
  <nav class="pagination" aria-label="Navigasi halaman">
    <button
      type="button"
      :disabled="skip === 0 || loading"
      @click="$emit('previous')"
    >
      Sebelumnya
    </button>

    <span>
      Halaman {{ currentPage }} dari {{ totalPages }}
    </span>

    <button
      type="button"
      :disabled="skip + limit >= total || loading"
      @click="$emit('next')"
    >
      Berikutnya
    </button>
  </nav>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  skip: {
    type: Number,
    required: true,
  },
  limit: {
    type: Number,
    required: true,
  },
  total: {
    type: Number,
    required: true,
  },
  loading: {
    type: Boolean,
    required: true,
  },
})

defineEmits(["previous", "next"])

const currentPage = computed(() => {
  return Math.floor(props.skip / props.limit) + 1
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(props.total / props.limit))
})
</script>