<template>
  <div>
    <h1>Shows Today</h1>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useContentStore } from '@/stores/'

const contentStore = useContentStore()

onMounted(() => {
  contentStore.startAutoRefresh()
})

onUnmounted(() => {
  contentStore.stopAutoRefresh()
})
</script>
