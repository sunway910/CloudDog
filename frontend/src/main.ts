// https://unocss.dev/ 原子 css 库
import '@unocss/reset/tailwind-compat.css' // unocss reset
import 'virtual:uno.css'
import 'virtual:unocss-devtools'

// 你自定义的 css
import './styles/main.css'

import App from './App.vue'

const app = createApp(App)

app.mount('#app')

//
// import { createApp } from "vue"
// import App from "./App.vue"
// import router from "./router"
//
// URLSearchParams.prototype.appendIfExists = function (key, value) {
//     if (value !== null && value !== undefined) {
//         this.append(key, value)
//     }
// }
//
// createApp(App).use(router).mount("#app")
