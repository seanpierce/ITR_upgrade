import { defineStore } from 'pinia'
import { ref, onUnmounted } from 'vue'
import { fetchContent } from '@/services/content'
import type { MarqueeResponse } from '@/types'

export const useContentStore = defineStore('content', () => {
  const marqueeText = ref<string>('')
  const about = ref<MarqueeResponse['about']>(null)

  let refreshInterval: number | undefined

  const loadContent = async () => {
    try {
      const data = await fetchContent()
      marqueeText.value = data.marqueeText
      about.value = data.about
    } catch (err) {
      console.error('Failed to fetch content:', err)
    }
  }

  const startAutoRefresh = () => {
    // Immediately load content
    loadContent()

    // Refresh every 2 minutes (120000 ms)
    refreshInterval = window.setInterval(loadContent, 120000)
  }

  const stopAutoRefresh = () => {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = undefined
    }
  }

  // stop interval if/when store is no longer used
  onUnmounted(() => {
    stopAutoRefresh()
  })

  return {
    marqueeText,
    about,
    startAutoRefresh,
    stopAutoRefresh,
  }
})
