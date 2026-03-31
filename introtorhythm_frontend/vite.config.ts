import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(async ({ mode }) => {
  const devToolsPlugin =
    mode === 'development'
      ? (await import('vite-plugin-vue-devtools')).default()
      : null

  return {
    plugins: [
      vue(),
      ...(devToolsPlugin ? [devToolsPlugin] : []),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      watch: {
        usePolling: true,
        interval: 100, // optional, default ~100ms
      },
    },
  }
})