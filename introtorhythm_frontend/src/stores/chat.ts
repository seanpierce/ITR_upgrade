import { defineStore } from 'pinia';
import { ref } from 'vue';
import { io, Socket } from 'socket.io-client';
import { SocketConfig as sock, type ChatMessage } from '@/types';

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([]);
  const messageInput = ref('');
  const usernameInput = ref('');
  const username = ref<string | null>(null);
  const usernameError = ref<string | null>(null);
  let socket: Socket | null = null;

  const connect = (name: string) => {
    if (socket) socket.disconnect();

    const socketUrl = import.meta.env.VITE_SOCKET_URL;
    socket = io(socketUrl, { transports: ['websocket', 'polling'] });

    socket.on(sock.CONNECTION, () => {
      socket?.emit(sock.JOIN, name);
    });

    socket.on(sock.JOIN_SUCCESS, (uname: string) => {
      username.value = uname;
      usernameError.value = null;
      localStorage.setItem(sock.GET_LOCAL_USERNAME, uname);
    });

    socket.on(sock.JOIN_ERROR, (err: string) => {
      usernameError.value = err;
      username.value = null;
      socket?.disconnect();
    });

    socket.on(sock.CHAT_MESSAGES, (msgs: ChatMessage[]) => {
      // Filter out duplicates
      const messagesToPush = msgs.filter(
        (m) => !messages.value.find((existing) => existing.id === m.id),
      );
      messages.value.push(...messagesToPush);
    });
  };

  const sendMessage = () => {
    if (!messageInput.value.trim() || !socket || !username.value) return;
    socket.emit(sock.CHAT_MESSAGE, username.value, messageInput.value);
    messageInput.value = '';
  };

  const setUsername = () => {
    if (!usernameInput.value.trim()) return;
    connect(usernameInput.value.trim());
    usernameInput.value = '';
  };

  const unsetUsername = () => {
    if (!socket || !username.value) return;
    username.value = null;
    localStorage.removeItem(sock.GET_LOCAL_USERNAME);
    socket.emit(sock.LOGOUT);
  };

  const getUsernameFromLocalStorage = () => {
    const username = localStorage.getItem(sock.GET_LOCAL_USERNAME);
    if (username) {
      connect(username);
    }
  };

  return {
    messages,
    messageInput,
    usernameInput,
    username,
    usernameError,
    connect,
    sendMessage,
    setUsername,
    unsetUsername,
    getUsernameFromLocalStorage,
  };
});
