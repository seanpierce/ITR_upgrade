<template>
  <div id="chat">
    <div id="chat-wrapper">
      <!-- Username input form -->
      <div v-if="!username" class="new-user">
        <div class="new-user-form">
          <input
            type="text"
            v-model="chatStore.usernameInput"
            @keyup.enter="setUsername"
            placeholder="Enter your username"
            maxlength="200"
          />
          <!-- Show error if username is not unique -->
          <div v-if="usernameUniqueError" class="username-unique-error error">
            Username already exists. Please choose another one.
          </div>
          <button @click="setUsername">Join Chat</button>
        </div>
      </div>
      <!-- Chat messages and input -->
      <div v-if="username">
        <div id="messages">
          <div v-for="msg in messages" :key="msg.id" class="message">
            <span class="time-stamp">{{ msg.friendlyTime }}</span>
            <span :class="{ me: msg.username === username }">{{ msg.username }}</span
            >: {{ msg.text }}
          </div>
        </div>
        <div id="message-input">
          <input
            id="message-input-field"
            type="text"
            v-model="chatStore.messageInput"
            @keyup.enter="chatStore.sendMessage"
            placeholder="Say something..."
            maxlength="200"
          />
          <button @click="chatStore.sendMessage">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useChatStore } from '@/stores/chat';
import { storeToRefs } from 'pinia';

const chatStore = useChatStore();

const { username, messages } = storeToRefs(chatStore);
const usernameUniqueError = ref(false);

const setUsername = () => {
  usernameUniqueError.value = false;
  if (!chatStore.isUsernameUnique()) {
    usernameUniqueError.value = true;
    return;
  }
  chatStore.setUsername();
};

onMounted(() => {
  chatStore.connect();
});
</script>
