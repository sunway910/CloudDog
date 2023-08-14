import { defineStore } from 'pinia'

export default defineStore('description', {
	state() {
		return {
			description: 'Sunthy Cloud Technical Limited',
		}
	},
	actions: {
		redirect() {
			window.location.href="https://www.sunthycloud.com"
		},
	},
	persist: true,
})
