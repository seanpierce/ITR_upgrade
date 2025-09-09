import { defineStore } from 'pinia';
import { ref } from 'vue';
import { io, Socket } from 'socket.io-client';
import type { ChatMessage } from '@/types';

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([]);
  const messageInput = ref('');
  const usernameInput = ref('');
  const username = ref<string | null>(null);
  let socket: Socket | null = null;

  const connect = () => {
    const socketUrl = import.meta.env.VITE_SOCKET_URL;
    console.log('Connecting to Socket.IO server at', socketUrl);
    socket = io(socketUrl, {
      transports: ['websocket', 'polling'],
    });

    socket.on('connect', () => console.log('Connected to Socket.IO server'));

    socket.on('chatMessages', (msgs: ChatMessage[]) => {
      messages.value.push(...msgs);
    });
  };

  const sendMessage = () => {
    if (!messageInput.value.trim() || !socket) return;
    socket.emit('chatMessage', username.value, messageInput.value);
    messageInput.value = '';
  };

  const setUsername = () => {
    if (!usernameInput.value.trim() || !socket) return;
    username.value = usernameInput.value;
    usernameInput.value = '';
  };

  const isUsernameUnique = () => {
    const names = messages.value.map((m) => m.username?.toLowerCase());
    if (usernameInput.value && names.includes(usernameInput.value.toLowerCase())) {
      return false;
    }
    return true;
  };

  return {
    messages,
    messageInput,
    usernameInput,
    username,
    connect,
    sendMessage,
    setUsername,
    isUsernameUnique,
  };
});
