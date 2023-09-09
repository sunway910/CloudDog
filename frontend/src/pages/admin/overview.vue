<template>
	<div>
		<div class="product_container">
			<div class="handle-box">
				<el-select v-model="queryConditions.cloud_platform" placeholder="Cloud Platform" class="handle-select mr10">
					<el-option
						v-for="item in platformOptions"
						:key="item.value"
						:label="item.label"
						:value="item.value"
					/>
				</el-select>
				<el-input v-model="queryConditions.project_name" placeholder="Project Name" class="handle-input mr10"></el-input>
				<el-button :icon="Search" type="primary" @click="searchProjects">Search</el-button>
				<el-button :icon="Plus" type="primary" @click="handleCreate" v-auth=auth[0] style="float: right">New</el-button>
				<el-button :icon="Refresh" type="primary" @click="getProjectList" style="float: right">Refresh</el-button>
			</div>
			<el-table :data="projectList" border class="table" ref="multipleTable" header-cell-class-name="table-header">
				<el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
				<el-table-column prop="cloud_platform" align="center" label="Cloud Platform"></el-table-column>
				<el-table-column prop="account" align="center" label="Account" show-overflow-tooltip></el-table-column>
				<el-table-column prop="region" align="center" label="Region"></el-table-column>
				<el-table-column prop="project_name" align="center" label="Project Name" show-overflow-tooltip></el-table-column>
				<el-table-column label="Status" align="center">
					<template #default="scope">
						<el-tag :type="scope.row.status === 'Running' ? 'success' : scope.row.status === 'Stopped' ? 'danger' : ''">
							{{ scope.row.status }}
						</el-tag>
					</template>
				</el-table-column>
				<el-table-column prop="create_time" label="Create Time" align="center"></el-table-column>

				<el-table-column label="Operation" width="220" align="center">
					<template #default="scope">
						<el-button text :icon="Edit" @click="handleUpdate(scope.$index,scope.row)" v-auth=auth[0]>
							Edit
						</el-button>
						<el-button text :icon="Delete" class="red" @click="deleteProject(scope.row)" v-auth=auth[0]>
							Delete
						</el-button>
					</template>
				</el-table-column>

			</el-table>
			<div class="admin_pagination">
				<el-pagination
					background
					layout="total, prev, pager, next"
					:current-page="queryConditions.pageIndex"
					:page-size="queryConditions.pageSize"
					:total="pageTotal"
					@current-change="handlePageChange"
				></el-pagination>
			</div>
		</div>

		<!-- create or update project -->
		<el-dialog title="Edit" v-model="DialogVisible" width="40%">
			<el-form label-width="150px" v-model="createOrUpdateData">
				<el-form-item label="Cloud Platform">
					<el-select v-model="createOrUpdateData.cloud_platform" placeholder="Cloud Platform" class="handle-select mr10" :disabled="createOrUpdateRequest">
						<el-option
							v-for="item in platformOptions"
							:key="item.value"
							:label="item.label"
							:value="item.value"
						/>
					</el-select>
				</el-form-item>
				<el-tooltip content="multi account must split with blank" placement="top">
					<el-form-item label="Account" required>
						<el-input v-model="createOrUpdateData.account" placeholder="multi account must split with blank"></el-input>
					</el-form-item>
				</el-tooltip>
				<el-tooltip content="multi region must split with blank" placement="top">
					<el-form-item label="Region" required>
						<el-input v-model="createOrUpdateData.region" placeholder="multi region must split with blank"></el-input>
					</el-form-item>
				</el-tooltip>
				<el-form-item label="Project Name" required>
					<el-input v-model="createOrUpdateData.project_name" placeholder="Please input project name"></el-input>
				</el-form-item>
				<el-form-item label="Access Key" required v-show="!createOrUpdateRequest">
					<el-input v-model="createOrUpdateData.project_access_key" placeholder="Please input AK"></el-input>
				</el-form-item>
				<el-form-item label="Secret Key" required v-show="!createOrUpdateRequest">
					<el-input v-model="createOrUpdateData.project_secret_key" placeholder="Please input SK"></el-input>
				</el-form-item>
				<el-form-item label="Status" required>
					<el-select v-model="createOrUpdateData.status" placeholder="Cloud Platform" class="handle-select mr10">
						<el-option
							v-for="item in statusOptions"
							:key="item.value"
							:label="item.label"
							:value="item.value"
						/>
					</el-select>
				</el-form-item>
				<el-form-item label="Create time" required>
					<el-col :span="11">
						<el-form-item prop="create_time">
							<el-date-picker
								v-model="createOrUpdateData.create_time"
								type="date"
								label="Pick a date"
								placeholder="Pick a date"
								style="width: 100%"
								value-format="YYYY-MM-DD"
							/>
						</el-form-item>
					</el-col>
				</el-form-item>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="DialogVisible = false">Cancel</el-button>
					<el-button type="primary" @click="createOrUpdateProject">Confirm</el-button>
				</span>
			</template>
		</el-dialog>

	</div>
</template>

<script setup lang="ts">
import {ref, reactive} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import {Delete, Edit, Search, Plus, Refresh} from '@element-plus/icons-vue';
import router from "@/plugins/router";

const auth = ['admin', 'user']
const statusOptions = [
	{
		value: 'Running',
		label: 'Running',
	},
	{
		value: 'Stopped',
		label: 'Stopped',
	},
]
const platformOptions = [
	{
		value: 'All',
		label: 'All',
	},
	{
		value: 'AlibabaCloud',
		label: 'AlibabaCloud',
	},
	{
		value: 'Aliyun',
		label: 'Aliyun',
	},
	{
		value: 'AWS',
		label: 'AWS',
	},
	{
		value: 'Azure',
		label: 'Azure',
	},
	{
		value: 'GCP',
		label: 'GCP',
	},
]

// The pattern of Project
interface ProjectItem {
	id: any;
	cloud_platform: string;
	region: any;
	account: any;
	project_access_key: string,
	project_secret_key: string,
	project_name: string;
	status: string;
	create_time: string;
}

const projectList = ref<ProjectItem[]>([]);
const pageTotal = ref(0);

// The conditions of search api
const queryConditions = reactive({
	cloud_platform: "",
	project_name: "",
	pageIndex: 1,
	pageSize: 10,
});

const DialogVisible = ref(false); // el-dialog
const createOrUpdateRequest = ref(true);  // false means create request, true means update request
let idx: number = -1;

// create or update project
let createOrUpdateData = reactive<ProjectItem>({
	id: -1,
	cloud_platform: "",
	project_name: "",
	project_access_key: "",
	project_secret_key: "",
	region: "",
	account: "",
	status: "",
	create_time: "",
});

// get project list
const getProjectList = () => {
	sendGetReq({params: undefined, uri: "/project/list"}).then((res) => {
			res.data.data.map((item) => { // set account_list to account_string( the )
				let accountList = [];
				let regionList = [];
				for (let i = 0; i < item.account.length; i++) {
					accountList.push(item.account[i])
					regionList.push(item.region[i])
				}
				item.account = accountList.join(' ')
				item.region = regionList.join(' ')
			})
			pageTotal.value = parseInt(res.data.data.length)
			projectList.value = res.data.data
		}
	).catch((err) => {
		ElMessage.error(err || 'Get project list error');
	});
}
getProjectList(); // init project list

// search project by cloud_platform and project_name
const searchProjects = () => {
	sendGetReq({uri: "/project/detail", params: {cloud_platform: queryConditions.cloud_platform, project_name: queryConditions.project_name}}).then((res) => {
			pageTotal.value = parseInt(res.data.data.length)
			projectList.value = res.data.data
		}
	).catch((err) => {
		ElMessage.error(err || 'Search project error');
	});
}

const createOrUpdateProject = () => {

	if (!createOrUpdateRequest.value) {
		// ID is auto generated by postgresDB, create operation does not need param: id
		createOrUpdateData.id = null
	}

	createOrUpdateData.account = createOrUpdateData.account.toString().split(' ')
	createOrUpdateData.region = createOrUpdateData.region.toString().split(' ')

	sendPostReq({uri: "/project/create_or_update", payload: createOrUpdateData, config_obj: null}).then(() => {
		getProjectList() // create operation need to requery project list from db
	})

	if (createOrUpdateRequest.value) { // update operation, do not need to requery project list from db
		projectList.value[idx].project_name = createOrUpdateData.project_name;
		projectList.value[idx].account = createOrUpdateData.account;
		ElMessage.success(`${createOrUpdateRequest.value ? "Edit" : "Create"} project successfully`);
	}

	clearCreateOrUpdateData()  //clear data, set all attributes to ""
	DialogVisible.value = false // close dialog page
}

const deleteProject = (row: any) => {
	ElMessageBox.confirm('Are you sure you want to delete it', 'Message', {
		type: 'warning'
	})
		.then(() => {
			sendDeleteReq({uri: "/project/delete", params: {id: row.id}})
			ElMessage.success('delete successfully');
		})
		.catch(() => {
			ElMessage.error('delete failed');
		});
	getProjectList();
};

const handlePageChange = (val: number) => {
	queryConditions.pageIndex = val;
	getProjectList();
};

const handleUpdate = (index: number, row: any) => {
	idx = index;
	createOrUpdateData = row; // init data which should be updated
	DialogVisible.value = true; // open dialog page
	createOrUpdateRequest.value = true // set dialog mode to 'update'
};

const handleCreate = () => {
	clearCreateOrUpdateData()
	DialogVisible.value = true // open dialog page
	createOrUpdateRequest.value = false // set dialog mode to 'create'
};

const clearCreateOrUpdateData = () => {
	const keys = Object.keys(createOrUpdateData);
	let obj: { [name: string]: string } = {};
	keys.forEach((item) => {
		obj[item] = "";
	});
	Object.assign(createOrUpdateData, obj);
};

</script>

<style scoped>
.handle-box {
	margin-bottom: 20px;
}

.handle-select {
	width: 150px;
}

.handle-input {
	width: 300px;
}

.table {
	width: 100%;
	font-size: 14px;
}

.red {
	color: #F56C6C;
}

.mr10 {
	margin-right: 10px;
}

.product_container {
	padding: 30px;
	background: #fff;
	border: 1px solid #ddd;
	border-radius: 5px;
}

</style>
