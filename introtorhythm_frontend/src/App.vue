<template>
  <div id="container">
    <RouterView />
    <ChatRoom />
    <About />
  </div>
</template>

<script lang="ts" setup>
import ChatRoom from '@/components/ChatRoom.vue';
import About from '@/components/About.vue';
</script>