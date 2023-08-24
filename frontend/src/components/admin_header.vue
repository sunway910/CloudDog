<template>
	<div class="header">
<Expand/><Fold/>
		<div class="collapse-btn" @click="collapseChange">
			<el-icon v-if="sidebar.collapse">
				<Expand/>
			</el-icon>
			<el-icon v-else>
				<Fold/>
			</el-icon>
		</div>

		<div class="logo">后台管理系统</div>
		<div class="header-right">
			<div class="header-user-con">
				<!-- 消息中心 -->
				<div class="btn-bell" @click="router.push('/admin/tabs')">
					<el-tooltip
						effect="dark"
						:content="message_num ? `have ${message_num} messages unread` : `message center`"
						placement="bottom"
					>
						<!--						<i class="el-icon-lx-notice"></i>-->
						<el-icon>
							<Message/>
						</el-icon>
					</el-tooltip>
					<span class="btn-bell-badge" v-if="message_num"></span>
				</div>
				<!-- 用户头像 -->
				<el-avatar class="user-avator" :size="30" :src="imgurl"/>
				<!-- 用户名下拉菜单 -->
				<el-dropdown class="user-name" trigger="click" @command="handleCommand">
					<span class="el-dropdown-link">
						{{ username }}
						<el-icon class="el-icon--right">
							<arrow-down/>
						</el-icon>
					</span>
					<template #dropdown>
						<el-dropdown-menu>
							<a href="https://github.com/lin-xin/vue-manage-system" target="_blank">
								<el-dropdown-item>项目仓库</el-dropdown-item>
							</a>
							<el-dropdown-item command="user">个人中心</el-dropdown-item>
							<el-dropdown-item divided command="loginout">退出登录</el-dropdown-item>
						</el-dropdown-menu>
					</template>
				</el-dropdown>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import {onMounted} from 'vue';
import {useSidebarStore} from '@/stores/sidebar';
import {useRouter} from 'vue-router';
import imgurl from '/public/favicon.ico';

import {Expand, Fold, Message} from "@element-plus/icons-vue";

const username: string | null = localStorage.getItem('ms_username');
const message_num: number = 99;

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
	if (command == 'loginout') {
		localStorage.removeItem('ms_username');
		router.push('/login');
	} else if (command == 'user') {
		router.push('/user');
	}
};

</script>


<style scoped>
.header {
	position: relative;
	box-sizing: border-box;
	width: 100%;
	height: 70px;
	font-size: 22px;
	color: #fff;
}

.collapse-btn {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100%;
	float: left;
	padding: 0 21px;
	cursor: pointer;
}

.header .logo {
	float: left;
	width: 250px;
	line-height: 70px;
	color: #000000;
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


.btn-bell{
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
	color: #fff;
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

</style>
