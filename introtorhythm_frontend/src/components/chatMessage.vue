<template>
    <div class="message">
        <span class="time-stamp">{{ msg.friendlyTime }}</span>
        <span v-if="!isJoinLeaveMessage"class="username" :class="{ me: msg.username === username }">
            {{ msg.username }}
        </span>
        <span v-if="!isJoinLeaveMessage" class="message-content">: {{ msg.text }}</span>
        <span v-if="isJoinLeaveMessage" class="join-leave-content">{{ msg.text }}</span>
    </div>
</template>

<script lang="ts" setup>
import type { ChatMessage } from '@/types';
import { computed } from 'vue';

const props = defineProps<{
  msg: ChatMessage;
  username: string;
}>();

const isJoinLeaveMessage = computed(() => {
  return props.msg.isJoin || props.msg.isLeave;
});
</script>