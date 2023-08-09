<template>
  <nav
      aria-label="Site Nav"
      class="mx-auto h-80px max-w-3xl flex items-center justify-between p-4"
  >
		<span class="h-10 w-10 flex items-center justify-center">
			<SwitchIcon unmount-persets/>
		</span>

    <ul class="flex items-center gap-2 text-sm font-medium">
      <li v-for="r of routes" :key="r.path" class="hidden !block">
        <RouterLink class="rounded-lg px-3 py-2" :to="r.path">
          {{ t(r.name) }}
        </RouterLink>
      </li>

      <li>
        <a
            class="inline-flex items-center gap-2 rounded-lg px-3 py-2"
            href="https://github.com/dishait/tov-template"
            target="_blank"
        >
          <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
          >
            <mask id="lineMdGithubLoop0" width="24" height="24" x="0" y="0">
              <g fill="#fff">
                <ellipse cx="9.5" cy="9" rx="1.5" ry="1"/>
                <ellipse cx="14.5" cy="9" rx="1.5" ry="1"/>
              </g>
            </mask>
            <g
                fill="none"
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
            >
              <path
                  stroke-dasharray="30"
                  stroke-dashoffset="30"
                  d="M12 4C13.6683 4 14.6122 4.39991 15 4.5C15.5255 4.07463 16.9375 3 18.5 3C18.8438 4 18.7863 5.21921 18.5 6C19.25 7 19.5 8 19.5 9.5C19.5 11.6875 19.017 13.0822 18 14C16.983 14.9178 15.8887 15.3749 14.5 15.5C15.1506 16.038 15 17.3743 15 18C15 18.7256 15 21 15 21M12 4C10.3317 4 9.38784 4.39991 9 4.5C8.47455 4.07463 7.0625 3 5.5 3C5.15625 4 5.21371 5.21921 5.5 6C4.75 7 4.5 8 4.5 9.5C4.5 11.6875 4.98301 13.0822 6 14C7.01699 14.9178 8.1113 15.3749 9.5 15.5C8.84944 16.038 9 17.3743 9 18C9 18.7256 9 21 9 21"
              >
                <animate
                    fill="freeze"
                    attributeName="stroke-dashoffset"
                    dur="0.6s"
                    values="30;0"
                />
              </path>
              <path stroke-dasharray="10" stroke-dashoffset="10" d="M9 19">
                <animate
                    fill="freeze"
                    attributeName="stroke-dashoffset"
                    begin="0.7s"
                    dur="0.2s"
                    values="10;0"
                />
                <animate
                    attributeName="d"
                    dur="3s"
                    repeatCount="indefinite"
                    values="M9 19c-1.406 0-2.844-.563-3.688-1.188C4.47 17.188 4.22 16.157 3 15.5;M9 19c-1.406 0-3-.5-4-.5-.532 0-1 0-2-.5;M9 19c-1.406 0-2.844-.563-3.688-1.188C4.47 17.188 4.22 16.157 3 15.5"
                />
              </path>
            </g>
            <rect
                width="8"
                height="4"
                x="8"
                y="11"
                fill="currentColor"
                mask="url(#lineMdGithubLoop0)"
            >
              <animate
                  attributeName="y"
                  dur="10s"
                  keyTimes="0;0.45;0.46;0.54;0.55;1"
                  repeatCount="indefinite"
                  values="11;11;7;7;11;11"
              />
            </rect>
          </svg>
        </a>
      </li>

      <li class="hidden !block">
        <Dropdown/>
      </li>
    </ul>
  </nav>
  <div id="header">
    <div class="grid">
      <div></div>
      <h1 class="main-title">
        <router-link :to="{ name: 'Home' }">My Drf-Vue Blog</router-link>
      </h1>
      <SearchBox></SearchBox>
    </div>
    <hr />
    <div class="login">
      <div v-if="hasLogin">
        <div class="dropdown">
          <button class="dropbtn">欢迎, {{ uname }} !</button>
          <div class="dropdown-content">
            <router-link :to="{ name: 'UserCenter', params: { username: userName } }">
              用户中心
            </router-link>
            <router-link v-show="isSuperuser" :to="{ name: 'ArticleCreate' }">
              发表文章</router-link
            >
          </div>
        </div>
      </div>
      <div v-else>
        <router-link to="/login" class="login-link">注册/登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import SearchBox from "./SearchBox.vue"

import { ref, onMounted, computed } from "vue"
import authorization from "@/utils/authorization"

// import {getRoutes} from '@/router/index'
import {SwitchIcon} from 'vue-dark-switch'

const {t} = useI18n()

// const routes = getRoutes()
//     .filter((r) => !r.path.includes('notFound'))
//     .map((r) => {
//       let {path, name} = r
//       if (path === '/') {
//         return {path, name: 'Home'}
//       }
//
//       if (!name) {
//         name = path
//       }
//
//       return {path, name: name.toString().slice(1).replaceAll('/', ' · ')}
//     })
let userName = ref("")
let hasLogin = ref(false)
const isSuperuser = JSON.parse(localStorage.getItem("isSuperuser.myblog"))

const props = defineProps(["welcomeName"])

const uname = computed(() => {
  return props.welcomeName ? props.welcomeName : userName.value
})

if (hasLogin) {
  userName.value = localStorage.getItem("username.myblog")
}

onMounted(() => {
  authorization().then((data) => ([hasLogin.value, userName.value] = data))
})
</script>

<style scoped>
/* 样式来源: https://www.runoob.com/css/css-dropdowns.html* /
    /* 下拉按钮样式 */
.dropbtn {
  background-color: mediumslateblue;
  color: white;
  padding: 8px 8px 30px 8px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  height: 16px;
  border-radius: 5px;
}
/* 容器 <div> - 需要定位下拉内容 */
.dropdown {
  position: relative;
  display: inline-block;
}
/* 下拉内容 (默认隐藏) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 120px;
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
  text-align: center;
}
/* 下拉菜单的链接 */
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}
/* 鼠标移上去后修改下拉菜单链接颜色 */
.dropdown-content a:hover {
  background-color: #f1f1f1;
}
/* 在鼠标移上去后显示下拉菜单 */
.dropdown:hover .dropdown-content {
  display: block;
}
/* 当下拉内容显示后修改下拉按钮的背景颜色 */
.dropdown:hover .dropbtn {
  background-color: darkslateblue;
}
</style>

<style scoped>
#header {
  text-align: center;
  margin-top: 20px;
}

.main-title a {
  color: black;
  text-decoration: none;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 4fr 1fr;
}

.login-link {
  color: black;
}

.login {
  text-align: right;
  padding-right: 5px;
}
</style>
