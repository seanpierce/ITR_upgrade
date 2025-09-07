import express from 'express'
import http from 'http'
import { Server } from 'socket.io'
import cors from 'cors'

const app = express()
app.use(cors())

const server = http.createServer(app)
const io = new Server(server, {
  cors: { origin: '*' }
})

let messages: { id: number; text: string }[] = []

io.on('connection', (socket) => {
  console.log('User connected:', socket.id)
  socket.emit('chatMessages', messages)
  socket.join('general')

  socket.on('chatMessage', (msg) => {
    const messageData = { id: Date.now(), text: msg }
    messages.push(messageData)
    setTimeout(() => {
      messages = messages.filter(m => m.id !== messageData.id)
    }, 24 * 60 * 60 * 1000)
    io.to('general').emit('chatMessages', [messageData])
  })

  socket.on('disconnect', () => console.log('User disconnected:', socket.id))
})

server.listen(3000, () => console.log('Server running on port 3000'))
