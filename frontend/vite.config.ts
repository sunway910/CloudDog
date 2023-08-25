import {defineConfig} from "vite"
import preset from './presets'
import path from 'path'
import Vue from '@vitejs/plugin-vue'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

const pathSrc = path.resolve(__dirname, 'src')

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		preset(),
	],
	server: {
		port: 8080,
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"), // 路径别名
			"~": path.resolve(__dirname, "src"), // 路径别名
		},
		extensions: [".js", ".json", ".ts", "tsx"], // 使用路径别名时想要省略的后缀名
	},
})






