import { MockMethod } from 'vite-plugin-mock'
export default [
	// 用户登录
	{
		// 请求地址
		url: "/api/mock/user/login",
		// 请求方法
		method: "post",
		// 响应数据
		response: () => {
			return {
				code: 0,
				message: 'success',
				data: {
					token: "Token",
					username: "sunway",
					password: "123456"
				}
			}
		}
	},
	{
		url: '/api/mock/get',
		method: 'get',
		response: () => {
			return {
				code: 0,
				data: {
					name: 'mock',
				},
			}
		},
	},
	{
		url: '/api/mock/post',
		method: 'post',
		timeout: 2000,
		response: {
			code: 0,
			data: {
				name: 'mock',
			},
		},
	},
	{
		url: '/api/mock/text',
		method: 'post',
		rawResponse: async (req, res) => {
			let reqbody = ''
			await new Promise((resolve) => {
				req.on('data', (chunk) => {
					reqbody += chunk
				})
				req.on('end', () => resolve(undefined))
			})
			res.setHeader('Content-Type', 'text/plain')
			res.statusCode = 200
			res.end(`hello, ${reqbody}`)
		},
	},
] as MockMethod[]
