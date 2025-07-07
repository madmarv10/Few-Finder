import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true, // Allow external connections
    open: true, // Open browser on start
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
  define: {
    // Ensure environment variables are available
    'process.env': {}
  }
});
