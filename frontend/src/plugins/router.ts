import {createGetRoutes, setupLayouts} from 'virtual:meta-layouts'
import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import {routes as fileRoutes} from 'vue-router/auto/routes'
import {useAuthStore} from '@/stores/auth'
import {reactive} from 'vue'

declare module 'vue-router' {
    interface RouteMeta {
        name?: string
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
                name: route.name ? route.name.toString() : 'undefined',
                layout: 'admin_layout',
                ...route.meta,
                title: route.name
                    ? route.name.toString().split('/').pop()?.toUpperCase()
                    : 'No Title',
            },
        }
    } else {
        route = {
            ...route,
            meta: {
                name: route.name ? route.name.toString() : 'undefined',
                layout: 'index_default',
                ...route.meta,
                title: route.name
                    ? route.name.toString().split('/').pop()?.toUpperCase()
                    : 'No Title',
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
    } else {
        route = setLayoutsByCondition(route)
    }
    return route
}

const custom_layout_route_list = fileRoutes.map((route) => {
    // use recursive algorithm to set layout and title
    return recursiveLayouts(route)
})

export const router = createRouter({
    history: createWebHistory(),
    routes: setupLayouts(custom_layout_route_list),
})

export const getRoutes = createGetRoutes(router)

const expiredTime = atobDecode(localStorage.getItem('expiredTime'))


router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title}` != null ? `${to.meta.title}` : 'CloudDog'
    const auth = useAuthStore()
    let token = atobDecode(localStorage.getItem('access'))
    let now_time = new Date().getTime()
    let expire_time: number = -1
    if (!token && (to.path !== '/login' && to.path !== '/')) {
        next('/login')
    } else if (expiredTime !== null) {
        expire_time = parseInt(expiredTime)
        if (now_time >= expire_time) {
            localStorage.removeItem('access')
            localStorage.removeItem('expiredTime')
            next('/login')
        } else {
            next()
        }
    } else if (to.meta.permiss && !auth.key.includes(to.meta.permiss)) {
        next('/404');
    } else {
        next()
    }

})

export default router
