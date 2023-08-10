import vue from "@vitejs/plugin-vue"
import { resolve } from "path"
import { defineConfig } from "vite"
import Tov from './presets'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [Tov()],
  server: {
    port: 8080,
  },
  // resolve: {
  //   alias: {
  //     "@": path.resolve(__dirname, "src"), // 路径别名
  //     "~": path.resolve(__dirname, "src"), // 路径别名
  //   },
  //   extensions: [".js", ".json"], // 使用路径别名时想要省略的后缀名
  // },
})


