import { defineStore } from 'pinia'
import { onMounted, ref } from 'vue'

export const useScheduleStore = defineStore('schedule', () => {
    // State
    const currentShow = ref<string>();
    const upcomingShows = ref<string>();

    const getSchedule = async () => {
        // Fetch schedule data from an API or other source
        // For demonstration, we'll use static data
        currentShow.value = "Current Show Title";
        upcomingShows.value = "Upcoming Show Titles";
    }

    onMounted(() => {
        getSchedule();
    })

    return {
        currentShow,
        upcomingShows
    }
})