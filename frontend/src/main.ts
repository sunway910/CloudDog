// https://unocss.dev/ 原子 css 库
import '@unocss/reset/tailwind-compat.css' // unocss reset
import 'virtual:uno.css'
import 'virtual:unocss-devtools'
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import  "@element-plus/icons-vue";

// 你自定义的 css
import '@/styles/main.css'

import App from './App.vue'

const app = createApp(App)

// 注册element plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
	app.component(key, component);
}

app.mount('#app')
