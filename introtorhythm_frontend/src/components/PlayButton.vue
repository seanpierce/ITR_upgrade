<template>
  <button>
    <img
      v-if="!loading"
      :src="playing ? pauseButton : playButton"
      @click="toggleLive"
      alt="Intro To Rhythm Live play button"
      id="play-button"
    />
    <Spinner v-if="loading" />
  </button>
</template>

<script lang="ts" setup>
import { watch } from 'vue';
import Spinner from '@/components/Spinner.vue';
import { useLiveStore } from '@/stores/live';

// Static assets
import playButton from '@/assets/images/play-circle-orange.png';
import pauseButton from '@/assets/images/pause-circle-orange.png';
import { storeToRefs } from 'pinia';

// Live stream URL
const liveUrl = 'https://introtorhythm.com/stream';

// Pinia store
const liveStore = useLiveStore();
const { playing, loading,  } = storeToRefs(liveStore);

const toggleLive = () => {
    liveStore.toggleLive();
}

// Watch for changes to `playing` and start/stop audio
watch(playing, async (newVal: boolean) => {
  if (newVal) {
    await liveStore.setLiveAudio(liveUrl);
    liveStore.playLiveAudio();
  } else {
    liveStore.stopLiveAudio();
  }
});
</script>
