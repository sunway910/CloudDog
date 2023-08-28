import { defineStore } from 'pinia';

export const useSidebarStore = defineStore('sidebar', {
	state: () => {
		return {
			collapse: false
		};
	},
	getters: {},
	actions: {
		persist: true,
		handleCollapse() {
			this.collapse = !this.collapse;
		}
	}
});
