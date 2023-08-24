<template>
	<admin_header />

<!--	<admin_sidebar/>-->
<!--	<admin_tags />-->
<!--	<div class="content-box" :class="{ 'content-collapse': admin_sidebar.collapse }">-->
<!--		<v-tags></v-tags>-->
<!--		<div class="content">-->
<!--			<router-view v-slot="{ Component }">-->
<!--				<transition name="move" mode="out-in">-->
<!--					<keep-alive :include="admin_tags.nameList">-->
<!--						<component :is="Component"></component>-->
<!--					</keep-alive>-->
<!--				</transition>-->
<!--			</router-view>-->
<!--		</div>-->
<!--	</div>-->
<!--	<div class="w-screen flex flex-col items-center justify-center">-->
<!--		<router-view v-slot="{ Component }">-->
<!--			<transition name="fade" mode="out-in">-->
<!--				<component :is="Component" />-->
<!--			</transition>-->
<!--		</router-view>-->
<!--	</div>-->
	<Footer />
</template>

<script setup lang="ts">
import { useSidebarStore } from '@/stores/sidebar';
import { useTagsStore } from '@/stores/tags';

const admin_sidebar = useSidebarStore();
const admin_tags = useTagsStore();
</script>

<style scoped>

</style>
