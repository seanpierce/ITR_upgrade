import { fetchSchedule } from '@/services/content';
import { defineStore } from 'pinia'
import { onMounted, ref } from 'vue'

export const useContentStore = defineStore('content', () => {
    // State
    const currentShow = ref<string>();
    const upcomingShows = ref<string>();

    const getSchedule = async () => {
        const scheduleData = await fetchSchedule();
        currentShow.value = "Current Show Title";
        upcomingShows.value = "Upcoming Show Titles";
    }

    // Getters
    const getFullMarqueeText = () => '';

    onMounted(async () => {
        await getSchedule();
    });

    return {
        getFullMarqueeText
    }
})