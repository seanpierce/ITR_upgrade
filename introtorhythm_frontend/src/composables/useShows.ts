import { ref } from "vue";
import apiClient from '@/services/apiClient'

export interface Show {
  id: number;
  title: string;
  info: string;
  showImage: string;
  showFlyer: string;
  startDateTime: string;
  endDateTime: string;
}

export function useShows() {
  const shows = ref<Show[]>([]);
  const loading = ref(false);

  const fetchShows = async () => {
    loading.value = true;
    try {
      const response = await apiClient.get("/api/schedule/shows/");
      console.log(response?.data)
      shows.value = response?.data;
    } finally {
      loading.value = false;
    }
  };

  return { shows, loading, fetchShows };
}
