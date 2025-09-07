import type { MarqueeResponse } from "@/types";
import apiClient from "./apiClient";


export const fetchContent = async (): Promise<MarqueeResponse> => {
  try {
    return await apiClient.get<MarqueeResponse>('/api/content/');
  } catch (error) {
    console.error('Error fetching content:', error);
    throw error;
  }
};
