<template>
	<div class="sidebar">
		<el-menu
			class="sidebar-el-menu"
			:default-active="onRoutes"
			:collapse="sidebar.collapse"
			background-color="#324157"
			text-color="#bfcbd9"
			active-text-color="#20a0ff"
			unique-opened
			router
		>
			<template v-for="item in items">
				<template v-if="item.subs">
          <el-sub-menu :index="item.index" :key="item.index" v-auth="item.auth">
            <template #title>
              <el-icon>
                <component :is="item.icon"></component>
              </el-icon>
              <span>{{ item.title }}</span>
            </template>
            <template v-for="subItem in item.subs">
              <el-sub-menu v-if="subItem.subs" :index="subItem.index" :key="subItem.index" v-auth="item.auth">
                <template #title>{{ subItem.title }}</template>
                <el-menu-item v-for="(threeItem, i) in subItem.subs" :key="i" :index="threeItem.index">
                  {{ threeItem.title }}
                </el-menu-item>
              </el-sub-menu>
              <el-menu-item v-else :index="subItem.index" v-auth="item.auth">
                {{ subItem.title }}
              </el-menu-item>
            </template>
          </el-sub-menu>
        </template>
				<template v-else>
					<el-menu-item :index="item.index" :key="item.index" v-auth="item.auth">
						<el-icon>
							<component :is="item.icon"></component>
						</el-icon>
						<template #title>{{ item.title }}</template>
					</el-menu-item>
				</template>
			</template>
		</el-menu>
	</div>
</template>

<script setup lang="ts">
import {computed} from 'vue';
import {useSidebarStore} from '@/stores/sidebar';
import {useRoute} from 'vue-router';

const items = [
	{
		// icon : https://element-plus.org/en-US/component/icon.html
		icon: 'Odometer',
		index: '/admin',
		title: '系统首页',
		auth: 'user',
		subs: null,
	},
	{
		icon: 'Monitor',
		index: '2',
		title: '实例监控',
		auth: 'user',
		subs: [
			{
				index: '/admin/product/ecs',
				title: 'ECS监控',
				auth: 'user',
			},
			{
				index: '/admin/product/waf',
				title: 'WAF监控',
				auth: 'user',
			},
		],
	},
	{
		icon: 'DocumentCopy',
		title: '系统管理员',
		index: '3',
		auth: 'admin',
		subs: [
			{
				index: '/admin/system/cron',
				title: '定时任务',
				auth: 'admin',
			},
			{
				index: '/admin/system/messages',
				title: '系统消息',
				auth: 'admin',
			},
		],
	},
	{
		icon: 'Warning',
		title: '权限管理',
		index: '4',
		auth: 'admin',
		subs: [
			{
				index: '/admin/auth/auth',
				title: '用户权限管理',
				auth: 'admin',
			},
		],
	},
];

const route = useRoute();
const onRoutes = computed(() => {
	return route.path;
});

const sidebar = useSidebarStore();
</script>

<style scoped>
.sidebar {
	display: block;
	position: absolute;
	left: 0;
	top: 70px;
	bottom: 0;
	overflow-y: scroll;
}

.sidebar::-webkit-scrollbar {
	width: 0;
}

.sidebar-el-menu:not(.el-menu--collapse) {
	width: 250px;
}

.sidebar > ul {
	height: 100%;
}
</style>
