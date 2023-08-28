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
		data: {account: "sunway", password: "123456"},
		key: keys ? JSON.parse(keys) : <string[]>[],
		defaultList: <ObjectList>{
			admin: ['admin', 'user'],
			user: ['user']
		}
	}),
	// 定义 getters，等同于组件的计算属性
	getters: {
		// getter 函数接收 state 作为参数，推荐使用箭头函数
		hello: state => 'Hello!' + state.data.account
	},
	actions: {
		persist: true,
		async login(data: { account: string; password: string }) {
			try {
				// const res = sendPostReq({uri: "/token/", payload: data, config_obj: null}).then(
				// 	(res) => {
				let res = {data: {"access": "test", refresh: "test"}};
				// Date.parse(...) 返回1970年1月1日UTC以来的毫秒数
				// Token 被设置为1h，因此这里加上60000 * 60毫秒
				const expiredTime = Date.now() + 60000 * 60;
				localStorage.setItem("access", res.data.access);
				localStorage.setItem("refresh", res.data.refresh);
				localStorage.setItem("expiredTime", expiredTime.toString());
				localStorage.setItem("username", data.account);
				let resp = {data: {"is_superuser": "true"}};
				// const resp = sendGetReq({uri: "/user/${data.account}/"}).then((resp) => {
				localStorage.setItem("isSuperuser", resp.data.is_superuser);
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
					await router.push("/admin/overview");
					ElMessage.success('Sign in successfully');
				}
				const keys = this.defaultList[(data.account == 'admin' || data.account == 'sunway') ? 'admin' : 'user'];
				this.handleSet(keys);
				localStorage.setItem('permission', JSON.stringify(keys));
				// });
				// 	}
				// );
			} catch (error) {
				// 请检查用户名/密码是否正确
				ElMessage.error('Please check that the username/password is correct');
			}
		},
		logout() {
			this.data = {account: "", password: ""};
			localStorage.removeItem("access");
			localStorage.removeItem("refresh");
			localStorage.removeItem("expiredTime");
			localStorage.removeItem("username");
			localStorage.removeItem("isSuperuser");
			router.push("/").then(r => console.log("log out successfully"));
		},
		handleSet(val: string[]) {
			this.key = val;
		}
	}
});
