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
