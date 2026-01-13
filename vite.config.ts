import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@/game': resolve(__dirname, 'src/game'),
      '@/entities': resolve(__dirname, 'src/entities'),
      '@/physics': resolve(__dirname, 'src/physics'),
      '@/world': resolve(__dirname, 'src/world'),
      '@/levels': resolve(__dirname, 'src/levels'),
      '@/rendering': resolve(__dirname, 'src/rendering'),
      '@/input': resolve(__dirname, 'src/input'),
      '@/utils': resolve(__dirname, 'src/utils'),
      '@/rules': resolve(__dirname, 'src/rules'),
    }
  },
  server: {
    port: 3000,
    open: true
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html')
      }
    }
  }
})