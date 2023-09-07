<template>
	<div>
		<div class="product_container">
			<div class="handle-box">
				<el-select v-model="query.cloud_platform" placeholder="Cloud Platform" class="handle-select mr10">
					<el-option
						v-for="item in options"
						:key="item.value"
						:label="item.label"
						:value="item.value"
					/>
				</el-select>
				<el-input v-model="query.project_name" placeholder="Project Name" class="handle-input mr10"></el-input>
				<el-button :icon="Search" type="primary" @click="searchProjects">Search</el-button>
				<el-button :icon="Plus" type="primary">New</el-button>
			</div>
			<el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
				<el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
				<el-table-column prop="cloud_platform" align="center" label="Cloud Platform"></el-table-column>
				<el-table-column prop="account" align="center" label="Account" show-overflow-tooltip></el-table-column>
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
						<el-button text :icon="Edit" @click="handleEdit(scope.$index,scope.row)" v-auth=auth[0]>
							Edit
						</el-button>
						<el-button text :icon="Delete" class="red" @click="handleDelete(scope.$index)" v-auth=auth[0]>
							Delete
						</el-button>
					</template>
				</el-table-column>

			</el-table>
			<div class="admin_pagination">
				<el-pagination
					background
					layout="total, prev, pager, next"
					:current-page="query.pageIndex"
					:page-size="query.pageSize"
					:total="pageTotal"
					@current-change="handlePageChange"
				></el-pagination>
			</div>
		</div>

		<el-dialog title="Edit" v-model="editVisible" width="30%">
			<el-form label-width="100px">
				<el-form-item label="Project Name">
					<el-input v-model="editForm.project_name" placeholder="Please input project name"></el-input>
				</el-form-item>
				<el-form-item label="Account">
					<el-input v-model="editForm.account" placeholder="Multi account must split with blank"></el-input>
				</el-form-item>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="editVisible = false">Cancel</el-button>
					<el-button type="primary" @click="editProject">Confirm</el-button>
				</span>
			</template>
		</el-dialog>

	</div>
</template>

<script setup lang="ts">
import {ref, reactive} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import {Delete, Edit, Search, Plus} from '@element-plus/icons-vue';
import router from "~/plugins/router";

const auth = ['admin', 'user']

const options = [
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

interface TableItem {
	id: number;
	cloud_platform: string;
	account: string;
	project_name: string;
	status: string;
	create_time: string;
}

const query = reactive({
	cloud_platform: null,
	project_name: null,
	pageIndex: 1,
	pageSize: 10,
});


const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);
// 获取表格数据
const getProjectList = () => {
	sendGetReq({params: undefined, uri: "/project/list"}).then((res) => {
			pageTotal.value = parseInt(res.data.data.length)
			res.data.data.map((item) => {
				let accountList = [];
				for (let j = 0; j < item.account.length; j++) {
					accountList.push(item.account[j])
				}
				item.account = accountList.join(' ')
			})
			console.log("res.data.data", res.data.data)
			tableData.value = res.data.data
		}
	);
};
getProjectList();


const searchProjects = () => {
	sendGetReq({uri: "/project/detail", params: {cloud_platform: query.cloud_platform, project_name: query.project_name}}).then((res) => {
			console.log("res.data===========", res.data)
			pageTotal.value = parseInt(res.data.data.length)
			tableData.value = res.data.data
		}
	);
};

const handlePageChange = (val: number) => {
	query.pageIndex = val;
	getProjectList();
};

// 删除操作
const handleDelete = (index: number) => {
	// 二次确认删除
	ElMessageBox.confirm('Are you sure you want to delete it', 'Message', {
		type: 'warning'
	})
		.then(() => {
			ElMessage.success('delete successfully');
			tableData.value.splice(index, 1);
		})
		.catch(() => {
		});
};

// 表格编辑时弹窗和保存
let editData = ref<TableItem>();
const editVisible = ref(false);
let editForm = reactive({
	project_name: "",
	account: "",
});
let idx: number = -1;
const handleEdit = (index: number, row: any) => {
	idx = index;
	editVisible.value = true;
	editData.value = row;
	editForm.project_name = row.project_name;
	console.log("row.account========",row.account)
	editForm.account = row.account;
};
const editProject = () => {
	editVisible.value = false;
	if ("project_name" in editData.value) {
		editData.value.project_name = editForm.project_name;
	}
	if ("account" in editData.value) {
		editData.value.account = editForm.account;
	}
	console.log("after process edit data = \n", editData.value)
	sendPostReq({uri: "/project/update", payload: editData.value, config_obj: null}).then(
		(res) => {

		}
	)
	tableData.value[idx].project_name = editForm.project_name;
	tableData.value[idx].account = editForm.account;
	editData = ref<TableItem>();
	ElMessage.success(`edit row: ${idx + 1} successfully`);
}
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

.table-td-thumb {
	display: block;
	margin: auto;
	width: 40px;
	height: 40px;
}

.product_container {
	padding: 30px;
	background: #fff;
	border: 1px solid #ddd;
	border-radius: 5px;
}
</style>
