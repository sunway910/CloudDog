<script setup lang="ts">

const visible = ref(false);
const flag = ref("EN");

function dropdownHandler() {
	visible.value = false
}

const {availableLocales, locale} = useI18n()

function changeFlag(availableLocale) {
	locale.value = availableLocale
	console.log("availableLocale", availableLocale)
	if (availableLocale === "English") {
		flag.value = "EN"
	} else {
		flag.value = "CN"
	}
}

</script>

<!--// I18n-->
<template>
	<div class="relative">
		<div class="inline-flex items-center overflow-hidden rounded-md">
			<button
				style="color: #2563EB"
				class="h-full cursor-pointer border-0 bg-white p-2 text-gray-600 hover:bg-gray-200 hover:text-gray-700"
				:class="visible ? 'bg-gray-200 bg-gray-500 dark:bg-gray-500' : ''"
				@click.stop="visible = !visible"
			>{{ flag }}
			</button>
		</div>

		<Transition name="fade" mode="out-in">
			<div
				v-if="visible"
				@click="dropdownHandler"
				class="absolute end-0 z-10 mt-2 w-56 rounded-md bg-white shadow-lg divide-y divide-gray-100"
			>
				<div class="p-2">
					<span
						v-for="availableLocale of availableLocales"
						:key="availableLocale"
						:class="
							locale === availableLocale
								? 'bg-gray-100 text-gray-800 dark:bg-gray-400'
								: ''
						"
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
