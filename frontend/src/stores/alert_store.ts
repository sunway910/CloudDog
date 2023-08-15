import { defineStore } from "pinia";

export default defineStore("alert", {
  state() {
    return {
      alert: ""
    };
  },
  actions: {
    success(message: string) {
      this.alert = message;
    },
    error(message: string) {
      this.alert = message;
    },
    clear() {
      this.alert = null;
    }
  }
});
