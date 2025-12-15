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
          <div v-if="chatStore.usernameError" class="username-unique-error error">
            {{ chatStore.usernameError }}
          </div>
          <button @click="setUsername">Join Chat</button>
        </div>
      </div>

      <!-- Chat messages and input -->
      <div v-else>
        <div id="messages">
          <div id="messages-header">
            Username: <span class="red">{{ username }}</span> |
            <span @click="chatStore.unsetUsername" class="pointer bold logout">LOGOUT</span>
          </div>
          <div v-for="msg in messages" :key="msg.id" class="message">
            <span class="time-stamp">{{ msg.friendlyTime }}</span>
            <span class="username" :class="{ me: msg.username === username, isItr: msg.isItr }">{{
              msg.username
            }}</span
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
import { onMounted } from 'vue';
import { useChatStore } from '@/stores/chat';
import { storeToRefs } from 'pinia';

const chatStore = useChatStore();
const { username, messages } = storeToRefs(chatStore);

const setUsername = () => {
  // clear previous error
  chatStore.usernameError = null;
  chatStore.setUsername();
};

onMounted(() => {
  chatStore.getUsernameFromLocalStorage();
});
</script>
