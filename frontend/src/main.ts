// https://unocss.dev/ 原子 css 库
import '@unocss/reset/tailwind-compat.css' // unocss reset
import 'virtual:uno.css'
import 'virtual:unocss-devtools'
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import "@element-plus/icons-vue";
import {useAuthStore} from '@/stores/auth';

// custom css
import '@/styles/main.css'
import 'element-plus/dist/index.css';
import './assets/css/icon.css';

import App from './App.vue'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
	app.component(key, component)
}

// 自定义权限指令
const auth = useAuthStore();
app.directive('auth', {
	mounted(el, binding) {
		if (!auth.key.includes(String(binding.value))) {
            el['hidden'] = true;
        }
	},
});

app.mount('#app')
