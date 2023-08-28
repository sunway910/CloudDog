import {createGetRoutes, setupLayouts} from 'virtual:meta-layouts'
import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import {routes as fileRoutes} from 'vue-router/auto/routes'
import {useAuthStore} from '@/stores/auth';

declare module 'vue-router' {
	// 在这里定义你的 meta 类型
	interface RouteMeta {
		name? : string
		title?: string
		layout?: string
	}
}


function setLayoutsByCondition(route: RouteRecordRaw): RouteRecordRaw {

	// @ts-ignore
	if (route.name.includes('admin')) {
		route = {
			...route,
			meta: {
				name : route.name ? route.name.toString() : "undefined",
				layout: 'admin_layout', ...route.meta,
				title: route.name ? route.name.toString().split('/').pop()?.toUpperCase() : "No Title"
			},
		}
	} else {
		route = {
			...route,
			meta: {
				name : route.name ? route.name.toString() : "undefined",
				layout: 'index_default', ...route.meta,
				title: route.name ? route.name.toString().split('/').pop()?.toUpperCase() : "No Title"
			},
		}
	}
	return route
}

function recursiveLayouts(route: RouteRecordRaw): RouteRecordRaw {
	if (route.children) {
		for (let i = 0; i < route.children.length; i++) {
			route.children[i] = recursiveLayouts(route.children[i])
		}
	}else {
		route = setLayoutsByCondition(route)
	}
	return route
}

const custom_layout_route_list = fileRoutes.map((route) => {
	// use recursive algorithm to set layout and title
	return recursiveLayouts(route)
})

// console.log('custom_layout_route_list=', custom_layout_route_list)

export const router = createRouter({
	history: createWebHistory(),
	routes: setupLayouts(custom_layout_route_list),
})

export const getRoutes = createGetRoutes(router)

router.beforeEach((to, from, next) => {
	document.title = `${to.meta.title} | CloudPlatformMonitor`;
	const role = localStorage.getItem('username');
	const auth = useAuthStore();
	if (!role && to.path !== '/login') {
		next('/login');
	} else if (to.meta.permiss && !auth.key.includes(to.meta.permiss)) {
		// 如果没有权限，则进入403
		next('/404');
	} else {
		next();
	}
});

export default router
