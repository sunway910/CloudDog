<script setup lang="ts">
const typedRef = useTyped([' Permission deny'])
</script>

<template>
  <Navigation/>
	<div class="h-screen flex flex-wrap items-center justify-around text-center">
		<div class="desc font-blod">
			<div class="code text-7xl">403</div>
			<div ref="typedRef" class="content mb-5 text-2xl"> ! </div>
			<RouterLink to="/403">
				<button
					class="rounded bg-light-800 px-5 py-2 text-lg transition"
					hover="shadow-md"
					dark="text-black"
				>
					Go Home
				</button>
			</RouterLink>
		</div>

		<img src="/notFound/31.svg" class="cover" alt="page not found" />
	</div>
</template>

<style>
.code {
	margin-bottom: 20px;
}

.content {
	height: 40px;
}

.cover {
	height: auto;
	width: 700px;
	margin: 0 5px;
	max-width: 100%;
	max-height: 100%;
}

.desc {
	flex: 1;
	width: 300px;
}
</style>

<route lang="json">
{
	"meta": {
		"title": "403",
		"layout": "notFound"
	}
}
</route>
