import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import { SocketConfig as sock, type ChatMessage, type ChatUser } from '@/types';

const app = express();
app.use(cors());

const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

let messages: ChatMessage[] = [];
const users: Map<string, ChatUser> = new Map(); // username -> user
const disconnectTimers: Map<string, NodeJS.Timeout> = new Map();

const MESSAGE_LIMIT = 300;
const MESSAGE_TTL = 43200000; // 12 hours
const runPurgeTime = 300000; // 5 minutes
const DISCONNECT_GRACE = 5000; // 5 seconds

const getTimeOfMessage = (ms: number): string =>
  new Date(ms)
    .toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    .replace(/\s?[AP]M$/, '');

const purgeOldMessages = () => {
  const cutoff = Date.now() - MESSAGE_TTL;
  messages = messages.filter((m) => m.timestamp >= cutoff);
};

setInterval(purgeOldMessages, runPurgeTime);

// helper to broadcast system messages
const sendSystemMessage = (text: string) => {
  const now = Date.now();
  const msg: ChatMessage = {
    id: `system_${now}`,
    username: 'I2R',
    text,
    timestamp: now,
    friendlyTime: getTimeOfMessage(now),
    isItr: true,
  };
  messages.push(msg);
  console.log(messages, msg);
  io.to('general').emit(sock.CHAT_MESSAGES, [msg]);
};

io.on(sock.CONNECTION, (socket) => {
  // Send chat history on connect
  socket.emit(sock.CHAT_MESSAGES, messages);

  socket.join('general');

  // Handle join request
  socket.on(sock.JOIN, (username: string) => {
    if (!username) return;

    // If username already exists
    if (users.has(username)) {
      // Clear pending disconnect if this is a reconnect
      const timer = disconnectTimers.get(username);
      if (timer) {
        clearTimeout(timer);
        disconnectTimers.delete(username);
        users.set(username, { socketId: socket.id, username });
        socket.emit(sock.JOIN_SUCCESS, username);
        io.emit(sock.USER_LIST, Array.from(users.keys()));
        return;
      }

      socket.emit(sock.JOIN_ERROR, 'Username already taken');
      socket.disconnect();
      return;
    }

    // New user
    const newUser: ChatUser = { socketId: socket.id, username };
    users.set(username, newUser);

    io.emit(sock.USER_LIST, Array.from(users.keys()));
    socket.emit(sock.JOIN_SUCCESS, username);

    // System join message
    sendSystemMessage(`${username} has joined the chat`);
  });

  // Chat messages
  socket.on(sock.CHAT_MESSAGE, (username: string, msg: string, isItr = false) => {
    if (!users.has(username)) return;

    const now = Date.now();
    const messageData: ChatMessage = {
      id: `${socket.id}_${now}`,
      username,
      text: msg,
      timestamp: now,
      friendlyTime: getTimeOfMessage(now),
      isItr,
    };

    messages.push(messageData);
    if (messages.length > MESSAGE_LIMIT) {
      messages = messages.slice(-MESSAGE_LIMIT);
    }

    io.to('general').emit(sock.CHAT_MESSAGES, [messageData]);
  });

  // Logout handling.
  // This differs from disconnects as it is immediate.
  socket.on(sock.LOGOUT, () => {
    const user = Array.from(users.values()).find((u) => u.socketId === socket.id);
    if (!user) return;

    users.delete(user.username);
    io.emit(sock.USER_LIST, Array.from(users.keys()));
    sendSystemMessage(`${user.username} has left the chat`);
  });

  // Disconnect handling.
  // This differs from logout as it allows a grace period for reconnects.
  socket.on(sock.DISCONNECT, () => {
    const user = Array.from(users.values()).find((u) => u.socketId === socket.id);
    if (!user) return;

    // Start grace period before removing user
    const timer = setTimeout(() => {
      users.delete(user.username);
      disconnectTimers.delete(user.username);
      io.emit(sock.USER_LIST, Array.from(users.keys()));
      sendSystemMessage(`${user.username} has left the chat`);
    }, DISCONNECT_GRACE);

    disconnectTimers.set(user.username, timer);
  });
});

server.listen(3000, () => console.log('Server running on port 3000'));
