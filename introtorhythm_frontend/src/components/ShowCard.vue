<template>
  <div>
    <h2>{{ show.title }}</h2>
    <p>{{ show.info }}</p>
    <img v-if="show.showImage" :src="show.showImage" alt="show image" />
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import type { Show } from "../composables/useShows";

const props = defineProps<{ show: Show }>();
</script>
