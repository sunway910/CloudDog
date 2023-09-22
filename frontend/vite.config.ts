import { defineConfig } from 'vite'
import preset from './presets'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [preset()],
	server: {
		host: '0.0.0.0',
		port: 80,
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src'), // 路径别名
			'~': path.resolve(__dirname, 'src'), // 路径别名
		},
		extensions: ['.js', '.json', '.ts', 'tsx'], // 使用路径别名时想要省略的后缀名
	},
})






