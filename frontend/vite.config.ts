import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://0.0.0.0:8000',
      '/admin': 'http://0.0.0.0:8000',
      '/static/admin': 'http://0.0.0.0:8000',
    },
  },
});
