import {defineStore} from "pinia";
import router from "@/plugins/router";
import {ElMessage} from 'element-plus';

interface ObjectList {
    [key: string]: string[];
}

const keys = localStorage.getItem('permission')

export const useAuthStore = defineStore('auth', {
    state: () => ({
        // initialize state from local storage to enable user to stay logged in
        token: '',
        returnUrl: null,
        result: "",
        data: {username: "sunway", password: "123456"},
        key: keys ? JSON.parse(keys) : <string[]>[],
        defaultList: <ObjectList>{
            admin: ['admin', 'user'],
            user: ['user']
        }
    }),
    actions: {
        persist: true,
        login: async function (data: { username: string; password: string }) {
            try {
                sendPostReq({uri: "/token/", payload: data, config_obj: null}).then(
                    (res) => {
                        // Date.parse(...) 返回1970年1月1日UTC以来的毫秒数
                        // Token 被设置为1h，因此这里加上60000 * 60毫秒
                        const expiredTime = Date.now() + 60000 * 60;
                        localStorage.setItem("access", "Bearer " + res.data.access);
                        localStorage.setItem("refresh", res.data.refresh);
                        localStorage.setItem("expiredTime", expiredTime.toString());
                        localStorage.setItem("username", data.username);
                        const get_user_auth_uri: string = '/user/' + this.data.username + '/';
                        sendGetReq({params: undefined, uri: get_user_auth_uri}).then(async (resp) => {
                            localStorage.setItem("isSuperuser", resp.data.is_superuser);
                            const keys = this.defaultList[(data.username == 'admin' || data.username == 'sunway') ? 'admin' : 'user'];
                            this.handleSet(keys);
                            localStorage.setItem('permission', JSON.stringify(keys));
                            // 路由跳转，登录成功后跳转到
                            const {target} = router.currentRoute.value.query;
                            if (target) {
                                //  在vue3项目直接获取router实例即可,vue2当中是this.$router
                                //  可以通过currentRoute获取路由信息
                                // 使用 encodeURIComponent() 方法可以对 URI 进行编码
                                // target有可能是string或LocationQueryValue ,target as string是指定类型
                                await router.push(decodeURIComponent(target as string));
                                ElMessage.success('Sign in successfully');
                            } else {
                                await router.push("/admin/dashboard");
                                ElMessage.success('Sign in successfully');
                            }
                        });
                    }
                );
            } catch (error) {
                ElMessage.error('Please check that the username/password is correct');
            }
        },
        logout() {
            this.data = {username: "", password: ""};
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            localStorage.removeItem("expiredTime");
            localStorage.removeItem("username");
            localStorage.removeItem("isSuperuser");
            localStorage.removeItem("ms_keys");
            this.key = null;
            router.push("/login").then(() => console.log("log out successfully"));
        },
        handleSet(val: string[]) {
            this.key = val;
        }
    }
});
