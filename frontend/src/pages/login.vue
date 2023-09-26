<template>
  <section class="mt-15 bg-white w-1/3 dark:bg-#E8EBF6" style="box-shadow: 0 0 25px #2b669a;">
    <div class="container px-4 mx-auto ">
      <div class="max-w-lg mx-auto ">
        <div class="text-center mb-8 ">
          <h2 class="mt-3 text-3xl md:text-4xl font-extrabold mb-2 dark:text-black">{{ t('signin') }}</h2>
        </div>
        <el-form action="" :rules="rules" :model="loginForm">
          <div class="mb-6">
            <label class="block mb-2 font-extrabold dark:text-white" for="">{{ t('username') }}</label>
            <input v-model="loginForm.username" class="dark:text-black inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 bg-white shadow border-2 border-indigo-900 rounded" type="text" placeholder="Please input your account">
          </div>
          <div class="mb-6">
            <label class="block mb-2 font-extrabold dark:text-black" for="">{{ t('password') }}</label>
            <input @keydown.enter="login" v-model="loginForm.password" class="dark:text-black inline-block w-full p-4 leading-6 text-lg font-extrabold placeholder-indigo-900 bg-white shadow border-2 border-indigo-900 rounded" type="password" placeholder="Please input your password">
          </div>
          <div class="flex flex-wrap -mx-4 mb-6 items-center justify-between">
            <div class="w-full lg:w-auto px-4 mb-4 lg:mb-0 dark:text-white text-black">
              <el-checkbox v-model="checked" style="font-weight: bold; color: black;font-size:20px">{{ t('remember') }}</el-checkbox>
            </div>
            <div class="w-full lg:w-auto px-4 mb-4 lg:mb-0">
            </div>
            <!--          <div class="w-full lg:w-auto px-4"><a class="inline-block font-extrabold hover:underline" href="#">Forgot your password?</a></div>-->
          </div>
          <button type="button" @click="login" class="inline-block w-full py-4 px-6 mb-6 text-center text-lg leading-6 text-white font-extrabold bg-indigo-800 hover:bg-indigo-900 border-3 border-indigo-900 shadow rounded transition duration-200">{{ t('signin') }}</button>
          <!--        <p class="text-center font-extrabold">Don&rsquo;t have an account? <a class="text-red-500 hover:underline" href="#">Sign up</a></p>-->
        </el-form>
      </div>
    </div>
  </section>
</template>

<script setup>

import {reactive} from 'vue'
import {useAuthStore} from "@/stores/auth"
import {useRouter} from "vue-router";

const {t, locale} = useI18n()
const router = useRouter();
let checked = true;


let loginForm = reactive({
  username: "sunway",
  password: "123456"
});

const rules = {
  username: [{required: true, message: "please enter username", trigger: "blur"}, {
    min: 5,
    max: 14,
    message: "5 to 14 characters in length",
    trigger: "blur"
  }],
  password: [{required: true, message: "please enter password", trigger: "blur"}, {
    min: 6,
    message: "Password length must be greater than 6",
    trigger: "blur"
  }]
};

// 实例化 store
const userStore = useAuthStore()

const login = async () => {
  // 使用 actions，当作函数一样直接调用
  // login action 定义为了 async 函数，所以它返回一个 Promise
  await userStore.login(loginForm)
}

</script>

<style scoped>
.loginContainer {
  border-radius: 15px;
  background-clip: padding-box;
  margin: 10% auto;
  width: 350px;
  padding: 15px 35px 15px 35px;
  box-shadow: 0 0 25px #2b669a;
}

.loginTitle {
  margin: 0 auto 48px auto;
  text-align: center;
  font-size: 40px;
}

.loginRemember {
  text-align: left;
  margin: 0 0 15px 0;
}

</style>
