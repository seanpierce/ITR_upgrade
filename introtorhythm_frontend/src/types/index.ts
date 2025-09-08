export interface MarqueeResponse {
  marqueeText: string;
  about: About | null;
}

export interface About {
  info: string;
}

export interface ChatMessage {
  timestamp: number;
  id: number;
  username?: string;
  text: string;
}