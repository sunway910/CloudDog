<template>
	<div class="container">
		<el-tabs v-model="message">
			<el-tab-pane :label="`Unread(${unreadMessageList.length})`" name="first">
				<div class="handle-box">
					<el-input v-model="queryConditions.project_name" @keydown.enter="searchMessages(status_unread)" placeholder="Project Name" class="handle-input mr10" style="width: 300px"></el-input>
					<el-button :icon="Search" type="primary" @click="searchMessages(status_unread)">Search</el-button>
					<el-button :icon="Refresh" type="primary" @click="getMessageWithStatus(status_unread)" style="float: right">Refresh
					</el-button>
				</div>
				<el-table :data="unreadMessageList" style="margin-top: 20px">
					<el-table-column align="center" label="Project Name" width="200px">
						<template #default="scope">
							<span class="message-title">{{ scope.row.project_name }}</span>
						</template>
					</el-table-column>
					<el-table-column align="center" prop="product_type" width="200px" label="Product Type"></el-table-column>
					<el-table-column align="center" prop="event_type" width="100px" label="Event Type"></el-table-column>
					<el-table-column align="center" prop="create_time" width="300px" label="Time of occurrence"></el-table-column>
					<el-table-column align="center" prop="event_message" width="900px" label="Event Message"></el-table-column>
					<el-table-column align="center" width="200px" label="Operation" fixed="right">
						<template #default="scope">
							<el-button size="small" @click="handleMark(scope.row,status_read)">Mark as read</el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-tab-pane>
			<el-tab-pane :label="`Unread(${readMessageList.length})`" name="second">
				<div class="handle-box">
					<el-input v-model="queryConditions.project_name" placeholder="Project Name" class="handle-input mr10" style="width: 300px"></el-input>
					<el-button :icon="Search" type="primary" @click="searchMessages(status_read)">Search</el-button>
					<el-button :icon="Refresh" type="primary" @click="getMessageWithStatus(status_read)" style="float: right">Refresh</el-button>
				</div>
				<el-table :data="readMessageList" style="margin-top: 20px">
					<el-table-column align="center" label="Project Name" width="200px">
						<template #default="scope">
							<span class="message-title">{{ scope.row.project_name }}</span>
						</template>
					</el-table-column>
					<el-table-column align="center" prop="product_type" width="200px" label="Product Type"></el-table-column>
					<el-table-column align="center" prop="event_type" width="100px" label="Event Type"></el-table-column>
					<el-table-column align="center" prop="create_time" width="300px" label="Time of occurrence"></el-table-column>
					<el-table-column align="center" prop="event_message" width="900px" label="Event Message"></el-table-column>
					<el-table-column align="center" width="200px" label="Operation" fixed="right">
						<template #default="scope">
							<el-button size="small" @click="handleMark(scope.row,status_trash)">Mark as trash</el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-tab-pane>
			<el-tab-pane :label="`Trash(${trashMessageList.length})`" name="third">
				<div class="handle-box">
					<el-input v-model="queryConditions.project_name" placeholder="Project Name" class="handle-input mr10" style="width: 300px"></el-input>
					<el-button :icon="Search" type="primary" @click="searchMessages(status_trash)">Search</el-button>
					<el-button :icon="Refresh" type="primary" @click="getMessageWithStatus(status_trash)" style="float: right">Refresh</el-button>
				</div>
				<el-table :data="trashMessageList" style="margin-top: 20px">
					<el-table-column align="center" label="Project Name" width="200px">
						<template #default="scope">
							<span class="message-title">{{ scope.row.project_name }}</span>
						</template>
					</el-table-column>
					<el-table-column align="center" prop="product_type" width="200px" label="Product Type"></el-table-column>
					<el-table-column align="center" prop="event_type" width="100px" label="Event Type"></el-table-column>
					<el-table-column align="center" prop="create_time" width="300px" label="Create Time"></el-table-column>
					<el-table-column align="center" prop="event_message" width="900px" label="Time of occurrence"></el-table-column>
					<el-table-column align="center" width="200px" label="Operation" v-if="auth.key.includes(String(role[0]))" fixed="right">
						<template #default="scope">
							<el-button size="small" @click="handleDelete(scope.row)">Delete</el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-tab-pane>
		</el-tabs>
	</div>
</template>

<script setup lang="ts">
import {ref, reactive} from 'vue';
import {Refresh, Search} from "@element-plus/icons-vue";
import {ElMessage, ElMessageBox} from 'element-plus'
import {useAuthStore} from "~/stores/auth";

const auth = useAuthStore();
const role = ['admin', 'user']
const message = ref('first');
const status_unread = ref("unread")
const status_read = ref("read")
const status_trash = ref("trash")

interface MessageItem {
	id: number;
	project_name: string;
	instance_id: string;
	create_time: string;
	event_message: any;
	event_type: string,
	product_type: any,
	status: string,
}

const UpdateMessageData = reactive({
	id: -1,
	status: "",
});

const currentPageIndex = ref(1);
const pageSize = ref(10);
const unreadMessageList = ref<MessageItem[]>([]);
const readMessageList = ref<MessageItem[]>([]);
const trashMessageList = ref<MessageItem[]>([]);
const unreadPageTotal = ref(0);
const readPageTotal = ref(0);
const trashPageTotal = ref(0);
const queryConditions = reactive({
	project_name: "",
});

getMessageWithStatus(status_unread.value)
getMessageWithStatus(status_read.value)
getMessageWithStatus(status_trash.value)


function getMessageWithStatus(status: string) {
	sendGetReq({
		uri: "/message/list",
		params: {
			status: status,
			page_index: currentPageIndex.value,
			page_size: pageSize.value
		}
	}).then((res) => {
			if (status === status_unread.value) {
				unreadPageTotal.value = parseInt(res.data.data.length)
				unreadMessageList.value = res.data.data
			} else if (status === status_read.value) {
				readPageTotal.value = parseInt(res.data.data.length)
				readMessageList.value = res.data.data
			} else if (status === status_trash.value) {
				trashPageTotal.value = parseInt(res.data.data.length)
				trashMessageList.value = res.data.data
			}

		}
	).catch((err) => {
		ElMessage.error(err || 'Get message list error');
	});
}


const searchMessages = (status: string) => {
	sendGetReq({
		uri: "/message/search",
		params: {
			status: status,
			project_name: queryConditions.project_name,
			page_index: currentPageIndex.value,
			page_size: pageSize.value,
		}
	}).then((res) => {
			unreadPageTotal.value = parseInt(res.data.data.length)
			if (status === status_unread.value) {
				unreadPageTotal.value = parseInt(res.data.data.length)
				unreadMessageList.value = res.data.data
			} else if (status === status_read.value) {
				readPageTotal.value = parseInt(res.data.data.length)
				readMessageList.value = res.data.data
			} else if (status === status_trash.value) {
				trashPageTotal.value = parseInt(res.data.data.length)
				trashMessageList.value = res.data.data
			}
			queryConditions.project_name = ""
		}
	).catch((err) => {
		ElMessage.error(err || 'Search message error');
	});
}

const handleMark = (row: any, status: string) => {
	UpdateMessageData.status = status
	UpdateMessageData.id = row.id
	sendPostReq({uri: "/message/update", payload: UpdateMessageData, config_obj: null}).then(() => {
		getMessageWithStatus(status_unread.value)
		getMessageWithStatus(status_read.value)
		getMessageWithStatus(status_trash.value)
	})
};

const handleDelete = (row: any) => {
	ElMessageBox.confirm(
		'Message will permanently delete the file. Continue?',
		'Warning',
		{
			confirmButtonText: 'OK',
			cancelButtonText: 'Cancel',
			type: 'warning',
		}
	)
		.then(() => {
			sendDeleteReq({
				uri: "/message/delete", params: {
					id: row.id,
				}
			}).then(() => {
				getMessageWithStatus(status_unread.value)
				getMessageWithStatus(status_read.value)
				getMessageWithStatus(status_trash.value)
			})
			ElMessage({
				type: 'success',
				message: 'Delete completed',
			})
		})
		.catch(() => {
			ElMessage({
				type: 'info',
				message: 'Delete canceled',
			})
		})

};

</script>

<style>
.message-title {
	font-weight: bold;
	cursor: pointer;
}

</style>
