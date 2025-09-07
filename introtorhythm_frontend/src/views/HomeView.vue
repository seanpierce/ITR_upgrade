<template>
    <div id="live" class="content clearfix">

        <div class="background-container">
            <img id="bg" :src="bg" alt="">
        </div>

        <PlayButton />

        <div id="actions">
            <a href="mailto:hello@introtorhythm.com">hello@introtorhythm.com</a><br>
            <a href="tel:9718018007">971-801-8007</a><br>
            <a href="#chat" @click.prevent="goDown()">Chat</a>
        </div>
        
        <Marquee v-if="marqueeText.length && showMarquee" :text="marqueeText" />
    </div>
</template>

<script setup lang="ts">
import bg from '@/assets/images/i2r-bg-big-tall.png';
import { nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useContentStore } from '@/stores/'
import { storeToRefs } from 'pinia'
import PlayButton from '@/components/PlayButton.vue';
import Marquee from '@/components/Marquee.vue';

const contentStore = useContentStore()
const { marqueeText } = storeToRefs(contentStore)
const compareMarqueeText = ref<string>('');
const showMarquee = ref<boolean>(true);

watch(marqueeText, async () => {
  if (compareMarqueeText.value != marqueeText.value)
    await forceRemount();
});

const forceRemount = async () => {
  showMarquee.value = false;
  await nextTick(() => {
    showMarquee.value = true;
  });
  compareMarqueeText.value = marqueeText.value;
}

const goDown = () => {
  document.getElementById('chat-wrapper')!.scrollIntoView({ block: 'end',  behavior: 'smooth' });
}

onMounted(() => {
  contentStore.startAutoRefresh()
})

onUnmounted(() => {
  contentStore.stopAutoRefresh()
})
</script>
