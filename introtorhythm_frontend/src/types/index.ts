export interface MarqueeResponse {
  marqueeText: string;
  about: About | null;
}

export interface About {
  info: string;
}