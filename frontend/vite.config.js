import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/mcp': {
        target: 'http://localhost:8080',
        changeOrigin: true
      },
      '/api': {
        target: 'http://localhost:8090',
        changeOrigin: true
      },
      '/healthz': {
        target: 'http://localhost:3000',
        changeOrigin: true
      }
    }
  }
});
