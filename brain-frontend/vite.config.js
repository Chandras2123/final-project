import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/

export default {
  server: {
    host: true,
    proxy: {
      "/upload": "http://192.168.0.15:8000",
      "/outputs": "http://192.168.0.15:8000"
    }
  }
}
