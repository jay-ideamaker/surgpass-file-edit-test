import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 6436,
    allowedHosts: ["surgpass-file-edit.logicadev.top"],
  },
});
