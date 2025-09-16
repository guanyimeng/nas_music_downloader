import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      "/auth": {
        target: "http://localhost:8000",
        changeOrigin: true
      },
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  },
  preview: {
    port: 5173
  }
});
