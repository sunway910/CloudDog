import {createGetRoutes, setupLayouts} from 'virtual:meta-layouts'
import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import {routes as fileRoutes} from 'vue-router/auto/routes'


declare module 'vue-router' {
	// 在这里定义你的 meta 类型
	interface RouteMeta {
		title?: string
		layout?: string
	}
}


function recursiveLayouts(route: RouteRecordRaw): RouteRecordRaw {
	if (route.children) {
		for (let i = 0; i < route.children.length; i++) {
			route.children[i] = recursiveLayouts(route.children[i])
		}
		return route
	}
	return setupLayouts([route])[0]
}

const custom_layout_route_list = fileRoutes.map((route) => {
	// My custom extendRoutes logic, that adds a meta field to force specific pages under
	// a given path to require auth.
	if (route.path.includes('admin')) {
		route = {
			...route,
			meta: {
				layout: 'admin_layout', ...route.meta,
			},
		}
	} else {
		route = {
			...route,
			meta: {
				layout: 'index_default', ...route.meta,
			},
		}
	}
	// For each route, pass it to recursiveLayouts, which will apply layouts properly
	// (without duplicating or accidentally double-wrapping components).
	// return recursiveLayouts(route)
	return route
})
// console.log('custom_layout_route_list=', custom_layout_route_list)
export const router = createRouter({
	history: createWebHistory(),
	routes: setupLayouts(custom_layout_route_list),
})

export const getRoutes = createGetRoutes(router)

export default router
