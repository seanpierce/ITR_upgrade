import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import type { ChatMessage } from '@/types';

const app = express();
app.use(cors());

const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: '*' },
});

let messages: ChatMessage[] = [];
const MESSAGE_LIMIT = 300;
const MESSAGE_TTL = 12 * 60 * 60 * 1000; // 12 hours in ms

function purgeOldMessages() {
  const cutoff = Date.now() - MESSAGE_TTL;
  messages = messages.filter((m: ChatMessage) => m.timestamp >= cutoff);
}

// Run purge every 5 minutes
setInterval(purgeOldMessages, 5 * 60 * 1000);

io.on('connection', (socket) => {
  console.log('User connected:', socket.id);
  socket.emit('chatMessages', messages);
  socket.join('general');

  socket.on('chatMessage', (msg) => {
    const messageData: ChatMessage = {
      id: Date.now(),
      username: 'User',
      text: msg,
      timestamp: Date.now(),
    };

    messages.push(messageData);

    if (messages.length > MESSAGE_LIMIT) {
      messages = messages.slice(-MESSAGE_LIMIT);
    }
    setTimeout(
      () => {
        messages = messages.filter((m) => m.id !== messageData.id);
      },
      24 * 60 * 60 * 1000,
    );
    io.to('general').emit('chatMessages', [messageData]);
  });

  socket.on('disconnect', () => console.log('User disconnected:', socket.id));
});

server.listen(3000, () => console.log('Server running on port 3000'));
