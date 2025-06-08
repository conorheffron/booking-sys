import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Add each path you want to proxy to the backend
      '/api': 'http://localhost:8000',
      '/admin': 'http://localhost:8000',
      // Add more as needed
    },
  },
});
