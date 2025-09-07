import { defineStore } from 'pinia';
import { ref } from 'vue';
import { LiveService } from '@/services/live';

export const useLiveStore = defineStore('live', () => {
  const playing = ref(false);
  const loading = ref(false);
  const volume = ref(0.8);
  const audio = ref<HTMLAudioElement | null>(null);

  const liveService = new LiveService(volume.value);

  // Actions
  function toggleLive() {
    playing.value = !playing.value;
  }

  function setVolume(newVolume: number) {
    const v = newVolume * 0.01;
    volume.value = v;
    liveService.setVolume(v);
  }

  async function setLiveAudio(url: string) {
    loading.value = true;
    audio.value?.pause();

    const onLoaded = () => {
      loading.value = false;
    };

    const onError = async () => {
      toggleLive();
      await setLiveAudio(url);
      toggleLive();
    };

    audio.value = liveService.setAudio(url, volume.value, onLoaded, onError);
  }

  function playLiveAudio() {
    liveService.play();
    playing.value = true;
  }

  function stopLiveAudio() {
    liveService.stop();
    playing.value = false;
    audio.value = null;
  }

  return {
    playing,
    loading,
    volume,
    audio,
    toggleLive,
    setVolume,
    setLiveAudio,
    playLiveAudio,
    stopLiveAudio,
  };
});
