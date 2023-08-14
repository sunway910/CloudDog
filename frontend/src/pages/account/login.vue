<template>
  <el-form :rules="rules" :model="loginForm" class="loginContainer">
    <h3 class="loginTitle">
      Sign in
    </h3>

    <el-form-item prop="username">
      <el-input type="text" v-model="loginForm.account" placeholder="Please input your account"></el-input>
    </el-form-item>

    <el-form-item prop="password">
      <el-input type="password" v-model="loginForm.password" placeholder="password" ></el-input>
    </el-form-item>

    <el-checkbox v-model="checked" class="loginRemember">remember me</el-checkbox>
    <el-button type="primary" style="width:100%" @click="signin">login in</el-button>

  </el-form>
</template>

<script setup>




async function onSubmit(values) {
  const authStore = useAuthStore();
  const { username, password } = values;
  await authStore.login(username, password);
}

import { useAuthStore } from '~/stores/index';
import { sendGetReq, sendPostReq } from "@/api/mock";
import { ref } from "vue";
import createUserStatus from "~/stores/createUserStatus";
import { useRouter } from "vue-router";

const router = useRouter();
let loginErr = ref("");
let checked = true;
// ref() 和 reactive() 用于跟踪其参数的更改。当使用它们初始化变量时，是向 Vue 提供信息：“嘿，每次这些变量发生更改时，请重新构建或重新运行依赖于它们的所有内容”
// ref() 函数可以接受原始类型（最常见的是布尔值、字符串和数字）以及对象作为参数，而 reactive() 函数只能接受对象作为参数。

let loginForm = reactive({
  account: "sunway",
  password: "123456"
});

const rules = {
  account: [{ required: true, message: "please enter account", trigger: "blur" }, {
    min: 5,
    max: 14,
    message: "5 to 14 characters in length",
    trigger: "blur"
  }],
  password: [{ required: true, message: "please enter password", trigger: "blur" }, {
    min: 6,
    message: "Password length must be greater than 6",
    trigger: "blur"
  }]
};

function signin() {
  router.push({ name: "/home" });
  sendPostReq({
    surl: "/token/",
    payload: { username: loginForm.account, password: loginForm.password },
    config_obj: null
  })
    .then((res) => {
      router.push({ name: "Home" });
      // 使用localStorage存储token
      const storage = localStorage;
      // Date.parse(...) 返回1970年1月1日UTC以来的毫秒数
      // Token 被设置为1h，因此这里加上60000 * 60毫秒
      const expiredTime = Date.now() + 60000 * 60;

      storage.setItem("access.monitor", res.data.access);
      storage.setItem("refresh.monitor", res.data.refresh);

      storage.setItem("expiredTime.monitor", expiredTime.toString());
      storage.setItem("username.monitor", loginForm.account);
      sendGetReq(`/user/${loginForm.account}/`).then((resp) => {
        storage.setItem("isSuperuser.monitor", resp.is_superuser);
        // 路由跳转，登录成功后跳转到首页
        router.push({ name: "/admin/overview" });
      });
    })
    .catch(() => {
      loginErr.value = "Please check the account and password are correct !";
      alert(loginErr.value);
    });
}

defineOptions({
  name: "LoginStatus"
});
const userStatus = createUserStatus();
</script>

<style scoped>
.loginContainer {
  border-radius: 15px;
  background-clip: padding-box;
  margin: 100px auto;
  width: 350px;
  padding: 15px 35px 15px 35px;
  background: white;
  border: 1px solid floralwhite;
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
