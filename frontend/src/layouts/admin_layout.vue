<template>
	<admin_header/>
	<admin_sidebar/>
	<div class="content-box" :class="{ 'content-collapse': sidebar.collapse }">
		<admin_tags/>
		<div class="content">
			<router-view v-slot="{ Component }">
				<transition name="move" mode="out-in">
					<keep-alive :include="tags.nameList">
						<component :is="Component"></component>
					</keep-alive>
				</transition>
			</router-view>
		</div>
	</div>
	<Footer/>
</template>

<script setup lang="ts">
import {useSidebarStore} from '@/stores/sidebar';
import {useTagsStore} from '@/stores/tags';

const sidebar = useSidebarStore();
const tags = useTagsStore();
</script>

<style scoped>
.content-box {
	position: absolute;
	left: 250px;
	right: 0;
	top: 70px;
	bottom: 0;
	padding-bottom: 30px;
	-webkit-transition: left .3s ease-in-out;
	transition: left .3s ease-in-out;
	background: #f0f0f0;
}
</style>
