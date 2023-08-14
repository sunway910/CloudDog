<template>
	<Navigation />
	<div class="w-screen flex flex-col items-center justify-center">
		<router-view v-slot="{ Component }">
			<transition name="fade" mode="out-in">
				<component :is="Component" />
			</transition>
		</router-view>
	</div>
	<Footer />
</template>

<style>
</style>

<script setup>
</script>
