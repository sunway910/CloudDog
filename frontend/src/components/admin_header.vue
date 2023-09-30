<template>
  <div class="admin_header bg-gray-800 text-white">
    <div class="admin_collapse-btn" @click="collapseChange" v-if="sidebar.collapse">
      <el-icon size="30">
        <Expand/>
      </el-icon>
    </div>
    <div class="admin_collapse-btn" v-else>
      <el-icon size="30">
        <Fold/>
      </el-icon>
    </div>
    <div class="admin_logo font-bold text-xl tracking-tight">CloudDog</div>
    <div class="header-right">
      <div class="header-user-con">
        <ul class="flex items-center gap-2 text-sm font-medium">
          <li class="hidden !block">
            <I18N/>
          </li>
        </ul>


        <div class="btn-bell" @click="router.push('/admin/system/messages')" style="margin-left: 10px">
          <el-tooltip
              effect="dark"
              :content="message_num ? `Have ${message_num} messages unread` : `Message Center`"
              placement="bottom">
            <el-icon color="white">
              <Message/>
            </el-icon>
          </el-tooltip>
          <span class="btn-bell-badge" v-if="message_num"></span>
        </div>

        <el-avatar class="user-avator" :size="30" :src="imgurl"/>

        <el-dropdown class="user-name" trigger="click" @command="handleCommand">
					<span class="el-dropdown-link">
						{{ username }}
						<el-icon class="el-icon--right">
							<arrow-down/>
						</el-icon>
					</span>
          <template #dropdown>
            <el-dropdown-menu>
              <a href="https://github.com/0utsiderZhong/CloudPlatformMonitor" target="_blank">
                <el-dropdown-item>Git Repo</el-dropdown-item>
              </a>
              <el-dropdown-item command="user">User Center</el-dropdown-item>
              <el-dropdown-item divided command="logout">Logout</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue';
import {useSidebarStore} from '@/stores/sidebar';
import {useRouter} from 'vue-router';
import imgurl from '/public/favicon.ico';

import {Expand, Fold, Message} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";

const username: string | null = atobDecode(localStorage.getItem('username'))
const message_num = ref(99);
const message_status = ref("unread");

const sidebar = useSidebarStore();
// 侧边栏折叠
const collapseChange = () => {
  sidebar.handleCollapse();
};

onMounted(() => {
  if (document.body.clientWidth < 1500) {
    collapseChange();
  }
});

// 用户名下拉菜单选择事件
const router = useRouter();
const handleCommand = (command: string) => {
  if (command == 'logout') {
    localStorage.removeItem('permission');
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('expiredTime');
    localStorage.removeItem('username');
    localStorage.removeItem('isSuperuser');
    router.push('/login');
  } else if (command == 'user') {
    router.push('/admin/auth/user');
  }
};

const getMessageWithStatus = (status: string) => {
  sendGetReq({
    uri: "/message/list",
    params: {
      status: status,
    }
  }).then((res) => {
        message_num.value = parseInt(res.data.data.length)
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get message list error');
  });
}
getMessageWithStatus(message_status.value)

</script>


<style scoped>
.admin_header {
  position: relative;
  box-sizing: border-box;
  width: 100%;
  height: 70px;
}

.admin_collapse-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  float: left;
  padding: 0 21px;
  cursor: pointer;
}

.admin_header .admin_logo {
  float: left;
  width: 300px;
  line-height: 70px;
  color: white;
}

.header-right {
  float: right;
  padding-right: 50px;
}

.header-user-con {
  display: flex;
  height: 70px;
  align-items: center;
}

.btn-bell,
.btn-fullscreen {
  position: relative;
  width: 30px;
  height: 30px;
  text-align: center;
  border-radius: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.btn-bell-badge {
  position: absolute;
  right: 4px;
  top: 0;
  width: 8px;
  height: 8px;
  border-radius: 4px;
  background: #f56c6c;
  color: #fff;
}

.btn-bell {
  color: #000000;
}

.user-name {
  margin-left: 10px;
}

.user-avator {
  margin-left: 20px;
}

.el-dropdown-link {
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.el-dropdown-menu__item {
  text-align: center;
}
</style>
