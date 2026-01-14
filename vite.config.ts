import { defineConfig } from 'vite'
import { resolve } from 'path'
import terser from '@rollup/plugin-terser'

export default defineConfig({
  base: '/icer/',
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
    sourcemap: false, // Disable sourcemaps for obfuscation
    minify: 'terser',
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html')
      },
      plugins: [
        terser({
          compress: {
            drop_console: true, // Remove console.log statements
            drop_debugger: true, // Remove debugger statements
            pure_funcs: ['console.log', 'console.info', 'console.debug', 'console.warn'],
            passes: 2, // Multiple compression passes
          },
          mangle: {
            toplevel: true, // Mangle top-level variable names
            properties: {
              regex: /^_/, // Mangle private properties starting with _
            },
            reserved: ['Game', 'Player', 'PIXI'], // Reserve important names
          },
          format: {
            comments: false, // Remove all comments
          },
        })
      ]
    }
  }
})