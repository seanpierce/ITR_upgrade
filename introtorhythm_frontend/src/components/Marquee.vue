<template>
    <div class="marquee-wrapper">
        <div id="live-marquee" class="marquee">
            {{ text }}
        </div>
    </div>
</template>

<script setup lang="ts">
import nodeMarquee from 'node-marquee';
import { onMounted } from 'vue';

const props = defineProps({
    text: {
        type: String,
        required: true,
        default: ''
    }
});

onMounted(() => {
    nodeMarquee({
        parent: '#live-marquee',
        pauseOnHover: true,
        speed: 4
    })});
</script>