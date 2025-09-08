import { defineStore } from 'pinia'
import { ref } from 'vue'
import { io, Socket } from 'socket.io-client'

interface Message {
  id: number
  text: string
}

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([]);
  const messageInput = ref('')
  let socket: Socket | null = null

  const connect = () => {
    const socketUrl = import.meta.env.VITE_SOCKET_URL
    socket = io(socketUrl, {
      transports: ['websocket']
    })

    socket.on('connect', () => console.log('Connected to Socket.IO server'))

    socket.on('chatMessages', (msgs: Message[]) => {
      messages.value.push(...msgs)
    })
  }

  const sendMessage = () => {
    if (!messageInput.value.trim() || !socket) return;
    socket.emit('chatMessage', messageInput.value);
    messageInput.value = '';
  }

  return { messages, messageInput, connect, sendMessage }
})
