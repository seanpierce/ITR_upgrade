export interface MarqueeResponse {
  marqueeText: string;
  about: About | null;
}

export interface About {
  info: string;
}

export interface ChatMessage {
  id: string;
  username: string;
  text: string;
  isItr: boolean;
  timestamp: number;
  friendlyTime: string;
}

export interface ChatUser {
  socketId: string;
  username: string;
}

export const SocketConfig = {
  CONNECTION: 'connection',
  DISCONNECT: 'disconnect',
  CHAT_MESSAGES: 'chatMessages',
  JOIN: 'join',
  JOIN_SUCCESS: 'joinSuccess',
  JOIN_ERROR: 'joinError',
  CHAT_MESSAGE: 'chatMessage',
  LOGOUT: 'logout',
  GET_LOCAL_USERNAME: 'chatUsername',
  USER_LIST: 'userList',
};
