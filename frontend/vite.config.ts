import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'https://booking-sys-ebgefrdmh3afbhee.northeurope-01.azurewebsites.net',
      '/admin': 'https://booking-sys-ebgefrdmh3afbhee.northeurope-01.azurewebsites.net',
      '/static/admin': 'https://booking-sys-ebgefrdmh3afbhee.northeurope-01.azurewebsites.net',
    },
  },
});
