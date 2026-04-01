import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/ask": "http://127.0.0.1:8000",
      "/upload-doc": "http://127.0.0.1:8000",
      "/create-vector-store": "http://127.0.0.1:8000",
      "/load-docs": "http://127.0.0.1:8000",
      "/health": "http://127.0.0.1:8000",
      "/test": "http://127.0.0.1:8000",
    },
  },
});