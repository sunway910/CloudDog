<template>
	<div style="margin-top: 300px; margin-left: 15%">
		<button
			style="width: 400px;height: 100px;font-weight: bolder;color: #1e1e1e"
			class="inline-block cursor-pointer rounded from-pink-500 via-red-500 to-yellow-500 bg-gradient-to-r px-8 py-2 text-sm font-medium text-white transition !border-0 !outline-none"
			hover="scale-110 shadow-xl"
			@click="description.redirect()">
			{{ description.description }}
		</button>
	</div>
</template>

<script lang="ts" setup>

defineOptions({
	name: 'Description',
})
const description = createDescription()
</script>
