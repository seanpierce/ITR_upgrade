<template>
    <button>
        <img v-if="!loading"
            id="play-button"
            :src="playing ? pauseButton : playButton" 
            @click="toggleLive()"
            alt="Intro To Rhythm Live play button">

        <Spinner v-if="loading" />
    </button>
</template>

<script setup lang="ts">
import playButton from '@/assets/images/play-circle-orange.png';
import pauseButton from '@/assets/images/pause-circle-orange.png';
import { computed, watch } from 'vue';
const liveUrl = 'https://introtorhythm.com/stream';

import Spinner from './Spinner.vue';

const playing = computed(() => {
    return '' // this.$store.state.live.playing
}); 

const audio = computed(() => {
    return '' // this.$store.state.live.audio
});

const loading = computed(() => {
    return '' // this.$store.state.live.loading
});

const toggleLive = () => {
    // toggle live store or service method
}

watch(playing, async () => {
    if (playing.value) {
        // await store.setLiveAudio(liveUrl);
        // store.playLiveAudio();
    } else {
        // store.stopLiveAudio();
    }
});
</script>