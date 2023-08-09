import {createWebHistory, createRouter} from "vue-router"
// import {createGetRoutes, setupLayouts} from 'virtual:meta-layouts'
// import {routes as fileRoutes} from 'vue-router/auto/routes'

const routes = [
    {
        path: "/",
        name: "Home",
        component: () => import("@/views/Home.vue"),
    },
    {
        path: "/article/:id",
        name: "ArticleDetail",
        component: () => import("@/views/ArticleDetail.vue"),
    },
    {
        path: "/login",
        name: "Login",
        component: () => import("@/views/Login.vue"),
    },
    {
        path: "/user/:username",
        name: "UserCenter",
        component: () => import("@/views/UserCenter.vue"),
    },
    {
        path: "/article/create",
        name: "ArticleCreate",
        component: () => import("@/views/ArticleCreate.vue"),
    },
    {
        path: "/article/edit/:id",
        name: "ArticleEdit",
        component: () => import("@/views/ArticleEdit.vue"),
    },
]

export const router = createRouter({
    history: createWebHistory(),
    // routes: setupLayouts(fileRoutes),
})
// export const getRoutes = createGetRoutes(router)

export default router
