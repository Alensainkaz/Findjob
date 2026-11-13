import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Builds one JS + one CSS file into Django's static/dist (served by WhiteNoise).
export default defineConfig({
  plugins: [vue()],
  base: '/static/dist/',
  build: {
    outDir: fileURLToPath(new URL('../static/dist', import.meta.url)),
    emptyOutDir: true,
    cssCodeSplit: false,
    rollupOptions: {
      input: fileURLToPath(new URL('./src/main.js', import.meta.url)),
      output: {
        entryFileNames: 'app.js',
        assetFileNames: 'app[extname]',
      },
    },
  },
})
