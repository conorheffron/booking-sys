import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://172.205.97.71:8000',
      '/admin': 'http://172.205.97.71:8000',
      '/static/admin': 'http://172.205.97.71:8000',
    },
  },
});
