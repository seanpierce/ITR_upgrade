<template>
  <div id="container">
    <RouterView />
    <About />
  </div>
</template>

<script lang="ts" setup>
import About from '@/components/About.vue';
</script>