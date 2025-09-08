<template>
<div id="chat">
    <div id="chat-wrapper">
        <div id="messages">
            <div v-for="msg in chatStore.messages" :key="msg.id" class="message">
                {{ msg.text }}
            </div>
        </div>
        <div id="message-input">
            <input
                type="text"
                v-model="chatStore.messageInput"
                @keyup.enter="chatStore.sendMessage"
                placeholder="Say something..."
            />
            <button @click="chatStore.sendMessage">Send</button>
        </div>
    </div>
</div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()

onMounted(() => {
  chatStore.connect()
})
</script>
