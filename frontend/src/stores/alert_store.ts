import { defineStore } from 'pinia';

export const useAlertStore = defineStore('alert',{
    state() {
		return {
            message: '',
			alert: '',
		}
	},
    actions: {
        success() {
            this.alert = 'alert-success' ;
        },
        error() {
            this.alert = 'alert-danger' ;
        },
        clear() {
            this.alert = 'null';
        }
    }
});



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
