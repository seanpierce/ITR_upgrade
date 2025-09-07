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
import { storeToRefs } from 'pinia';

import playButton from '@/assets/images/play-circle-orange.png';
import pauseButton from '@/assets/images/pause-circle-orange.png';

const liveStore = useLiveStore();
const { playing, loading } = storeToRefs(liveStore);
const liveUrl = 'https://introtorhythm.com/stream';

const toggleLive = () => {
    liveStore.toggleLive();
}

watch(playing, async (newVal: boolean) => {
  if (newVal) {
    await liveStore.setLiveAudio(liveUrl);
    liveStore.playLiveAudio();
  } else {
    liveStore.stopLiveAudio();
  }
});
</script>
