<script setup lang="ts">
import {ref} from "vue"
import {vOnClickOutside} from '@vueuse/components'

const visible = ref(false)
const flag = ref('EN')

function dropdownHandler() {
  visible.value = false
}

const {availableLocales, locale} = useI18n()

function changeFlag(availableLocale) {
  locale.value = availableLocale
  if (availableLocale === 'English') {
    flag.value = 'EN'
  } else {
    flag.value = 'CN'
  }
}
</script>

<!--// I18n-->
<template>
  <div class="relative">
		<span
        class="p-1 font-medium text-white-900 dark:text-gray-100 dark:bg-black-500 sm:p-4 cursor-pointer border-0 rounded-lg"
        :class="visible? 'text-gray-900 bg-white-500 dark:text-black-900 dark:bg-black-500': ''"
        @click.stop="visible = !visible">
      {{ flag }}
		</span>

    <Transition name="fade" mode="out-in">
      <div
          v-if="visible"
          @click="dropdownHandler"
          class="absolute end-0 z-10 mt-2 w-56 rounded-md bg-white text-black-500 dark:bg-black dark:text-white-500 shadow-lg divide-y divide-gray-100">
        <div class="p-2">
					<span
              v-for="availableLocale of availableLocales"
              :key="availableLocale"
              class="block cursor-pointer rounded-lg px-4 py-2 text-sm text-gray-500 hover:text-gray-900"
              dark="text-light-500 hover:text-light-900"
              @click="changeFlag(availableLocale)">
						{{ availableLocale }}
					</span>
        </div>
      </div>
    </Transition>
  </div>
</template>
