<template>
  <nav x-data="{ isOpen: false }" class="relative bg-white shadow dark:bg-gray-800">
    <div class="container px-6 py-4 mx-auto">
      <div class="lg:flex lg:items-center lg:justify-between">
        <div class="flex items-center justify-between">
          <a href="#">
            <img class="w-auto h-6 sm:h-15 " src="/favicon.ico" alt=""/>
          </a>
        </div>

        <div x-cloak
             class="translate-x-0 opacity-100 absolute inset-x-0 z-20 w-full px-6 py-4 transition-all duration-300 ease-in-out bg-white dark:bg-gray-800 lg:mt-0 lg:p-0 lg:top-0 lg:relative lg:bg-transparent lg:w-auto lg:opacity-100 lg:translate-x-0 lg:flex lg:items-center">
          <div class="flex flex-col -mx-6 lg:flex-row lg:items-center lg:mx-8">
            <a href="https://www.sunthycloud.com/"
               class="px-3 py-2 mx-3 mt-2 text-gray-700 transition-colors duration-300 transform rounded-md lg:mt-0 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">
              {{ t('about') }}
            </a>
            <a href="#" class="px-3 py-2 mx-3 mt-2 text-gray-700 transition-colors duration-300 transform rounded-md lg:mt-0 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
               to="/admin/dashboard">
              <RouterLink to="/admin/dashboard">
                {{ t('admin') }}
              </RouterLink>
            </a>
            <a class="px-3 py-2 mx-3 mt-2 text-gray-700 transition-colors duration-300 transform rounded-md lg:mt-0 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">
              <RouterLink to="login">
                {{ t('login') }}
              </RouterLink>
            </a>
            <a class="inline-flex items-center gap-2 rounded-lg px-3" href="https://github.com/0utsiderZhong/CloudPlatformMonitor" target="_blank">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <mask id="lineMdGithubLoop0" width="24" height="24" x="0" y="0">
                  <g fill="#fff">
                    <ellipse cx="9.5" cy="9" rx="1.5" ry="1"/>
                    <ellipse cx="14.5" cy="9" rx="1.5" ry="1"/>
                  </g>
                </mask>
                <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                  <path stroke-dasharray="30" stroke-dashoffset="30"
                        d="M12 4C13.6683 4 14.6122 4.39991 15 4.5C15.5255 4.07463 16.9375 3 18.5 3C18.8438 4 18.7863 5.21921 18.5 6C19.25 7 19.5 8 19.5 9.5C19.5 11.6875 19.017 13.0822 18 14C16.983 14.9178 15.8887 15.3749 14.5 15.5C15.1506 16.038 15 17.3743 15 18C15 18.7256 15 21 15 21M12 4C10.3317 4 9.38784 4.39991 9 4.5C8.47455 4.07463 7.0625 3 5.5 3C5.15625 4 5.21371 5.21921 5.5 6C4.75 7 4.5 8 4.5 9.5C4.5 11.6875 4.98301 13.0822 6 14C7.01699 14.9178 8.1113 15.3749 9.5 15.5C8.84944 16.038 9 17.3743 9 18C9 18.7256 9 21 9 21">
                    <animate fill="freeze" attributeName="stroke-dashoffset" dur="0.6s" values="30;0"/>
                  </path>
                  <path stroke-dasharray="10" stroke-dashoffset="10" d="M9 19">
                    <animate fill="freeze" attributeName="stroke-dashoffset" begin="0.7s" dur="0.2s" values="10;0"/>
                    <animate
                        attributeName="d"
                        dur="3s"
                        repeatCount="indefinite"
                        values="M9 19c-1.406 0-2.844-.563-3.688-1.188C4.47 17.188 4.22 16.157 3 15.5;M9 19c-1.406 0-3-.5-4-.5-.532 0-1 0-2-.5;M9 19c-1.406 0-2.844-.563-3.688-1.188C4.47 17.188 4.22 16.157 3 15.5"/>
                  </path>
                </g>
                <rect width="8" height="4" x="8" y="11" fill="currentColor" mask="url(#lineMdGithubLoop0)">
                  <animate attributeName="y" dur="10s" keyTimes="0;0.45;0.46;0.54;0.55;1" repeatCount="indefinite" values="11;11;7;7;11;11"/>
                </rect>
              </svg>
            </a>
            <ul class="flex items-center gap-2 text-sm font-medium">
              <li class="hidden !block px-1">
                <I18N/>
              </li>
              <li class="h-10 w-10 flex items-center justify-center px-1">
                <SwitchIcon unmount-persets/>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import {SwitchIcon} from 'vue-dark-switch'
import {Switch} from 'vue-dark-switch'

const {t, locale} = useI18n()

const toggleLocale = () => {
  // locale.value 用来表示当前所属语言，可修改进行语言切换
  locale.value = locale.value === 'zh-CN' ? 'en' : 'zh-CN'
}
</script>

<style>
.logo {
  width: 10em;
  height: 10em;
  padding: 1.5rem;
  will-change: filter;
  transition: filter 300ms;
}
</style>
