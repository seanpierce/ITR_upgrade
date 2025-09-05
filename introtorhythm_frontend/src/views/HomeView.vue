<template>
  <div>
    <h1>Shows Today</h1>
    <ShowCard v-for="show in shows" :key="show.id" :show="show" />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useShows } from "../composables/useShows";
import ShowCard from "@/components/ShowCard.vue";
const { shows, fetchShows } = useShows();

onMounted(() => {
  fetchShows();
});
</script>
