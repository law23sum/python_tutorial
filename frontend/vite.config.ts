import path from "path"
import { defineConfig } from 'vite'
import tailwindcss from "@tailwindcss/vite"
import react from '@vitejs/plugin-react-swc'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5174,
    // allow access to assets folder in the parent directory
    fs: {
      allow: ['..']
    }
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "assets": path.resolve(__dirname, "../assets"),
      "react/jsx-runtime": path.resolve(__dirname, "node_modules/react/jsx-runtime"),
      "react": path.resolve(__dirname, "node_modules/react"),
      "react-router-dom": path.resolve(__dirname, "node_modules/react-router-dom"),
      "api-client": path.resolve(__dirname, "../api-client"),
    },
  },
  build: {
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html'),
      },
      external: [],
    },
  },
  optimizeDeps: {
    include: ["api-client", "react", "react-dom", "react-router-dom", "react/jsx-runtime"],
    entries: [
      './src/**/*.{js,jsx,ts,tsx}',
      '../assets/javascript/**/*.{js,jsx,ts,tsx}'
    ]
  },
})
