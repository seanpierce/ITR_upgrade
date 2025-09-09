import { defineStore } from 'pinia';
import { ref } from 'vue';
import { io, Socket } from 'socket.io-client';
import type { ChatMessage } from '@/types';

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([]);
  const messageInput = ref('');
  const usernameInput = ref('');
  const username = ref<string | null>(null);
  const usernames = ref<string[]>([]);
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
    usernames.value.push(usernameInput.value);
    usernameInput.value = '';
    localStorage.setItem('chatUsername', username.value);
    sendITRMessage(`${username.value} has joined the chat`);
  };

  const unsetUsername = () => {
    if (!socket || !username.value) return;
    sendITRMessage(`${username.value} has left the chat`);
    usernames.value = usernames.value.filter((u) => u !== username.value);
    username.value = null;
    localStorage.removeItem('chatUsername');
  };

  const isUsernameUnique = () => {
    const names = messages.value.map((m) => m.username?.toLowerCase());
    if (usernameInput.value && names.includes(usernameInput.value.toLowerCase())) {
      return false;
    }
    return true;
  };

  const numberOfActiveUsers = () => {
    return usernames.value.length;
  };

  const getUsernameFromLocalStorage = () => {
    const storedUsername = localStorage.getItem('chatUsername');
    if (storedUsername) {
      usernameInput.value = storedUsername;
      setUsername();
    }
  };

  const sendITRMessage = (text: string) => {
    if (!socket) return;
    const isItr = true;
    socket.emit('chatMessage', 'ITR', text, isItr);
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
    unsetUsername,
    numberOfActiveUsers,
    getUsernameFromLocalStorage,
  };
});
