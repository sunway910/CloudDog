import axios from 'axios'

export const http = axios.create({
	baseURL: import.meta.env.VITE_API_BASE_URL,
})

http.interceptors.request.use(
	function (config) {
		config.headers['Content-Type'] = 'application/json'
		config.headers['Authorization'] = localStorage.getItem('access')
		if (config.method === 'post') {
			if (!config.data) {
				// 没有参数时，config.data为null，需要转下类型
				config.data = {}
			}
			config.data = JSON.stringify(config.data) // qs序列化参数
		}
		return config
	},
	function (error) {
		toast.warning(error.message ?? 'unknown request error')
		// 对请求错误做些什么
		return Promise.reject(error)
	},
)

// 添加响应拦截器
http.interceptors.response.use(
	function (response) {
		// 2xx 范围内的状态码都会触发该函数。
		// 对响应数据进行格式化
		// if (response.data) {
		// 	return response.data
		// }
		return response
	},
	function (error) {
		const status = error.response?.status
		let { msg, message } = error.response?.data ?? {}

		if (!msg && message) {
			msg = message
		}

		if (!msg) {
			switch (status) {
				case 400:
					msg = 'params error'
					break
				case 401:
					msg = 'auth error'
					break
				case 404:
					msg = 'page not found error'
					break
				case 500:
					msg = 'server error'
					break
				default:
					msg = error.message ?? 'unknown response error'
					break
			}
		}
		toast.warning(msg)
		// 超出 2xx 范围的状态码都会触发该函数。
		// 对响应错误做点什么
		return Promise.reject(error)
	},
)

export const sendGetReq = async ({
	uri,
	params,
}: {
	uri: string
	params: any
}) => {
	return await http.get(uri, { params: params })
}

export const sendPostReq = async ({
	uri,
	payload,
	config_obj,
}: {
	uri: string
	payload: any
	config_obj: any
}) => {
	return await http.post(uri, payload, config_obj)
}

export const sendPutReq = async ({
	uri,
	payload,
	config_obj,
}: {
	uri: string
	payload: any
	config_obj: any
}) => {
	return await http.put(uri, payload, config_obj)
}

export const sendPatchReq = async ({
	uri,
	payload,
	config_obj,
}: {
	uri: string
	payload: any
	config_obj: any
}) => {
	return await http.patch(uri, payload, config_obj)
}

export const sendDeleteReq = async ({
	uri,
	params,
}: {
	uri: string
	params: any
}) => {
	return await http.delete(uri, { params: params })
}
