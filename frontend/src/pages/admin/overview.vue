<template>
	<div>
		<div class="product_container">
			<div class="handle-box">
				<el-select v-model="query.name" placeholder="Cloud Platform" class="handle-select mr10">
					<el-option key="1" label="All" value="All"></el-option>
					<el-option key="1" label="Alibabacloud" value="Alibabacloud"></el-option>
					<el-option key="2" label="Aliyun" value="Aliyun"></el-option>
					<el-option key="2" label="AWS" value="AWS"></el-option>
					<el-option key="2" label="Azure" value="Azure"></el-option>
					<el-option key="2" label="GCP" value="GCP"></el-option>
				</el-select>
				<el-input v-model="query.name" placeholder="Project Name" class="handle-input mr10"></el-input>
				<el-button type="primary" :icon="Search" @click="handleSearch">Search</el-button>
				<el-button type="primary" :icon="Plus">New</el-button>
			</div>
			<el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
				<el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
				<el-table-column prop="cloud_platform" align="center" label="cloud_platform"></el-table-column>
				<el-table-column prop="account" align="center" label="account"></el-table-column>
				<el-table-column prop="project_name" align="center" label="project_name"></el-table-column>
				<el-table-column label="status" align="center">
					<template #default="scope">
						<el-tag :type="scope.row.status === 'Running' ? 'success' : scope.row.status === 'Stopped' ? 'danger' : ''">
							{{ scope.row.status }}
						</el-tag>
					</template>
				</el-table-column>
				<el-table-column prop="create_time" label="create_time" align="center"></el-table-column>

				<el-table-column label="操作" width="220" align="center">
					<template #default="scope">
						<el-button text :icon="Edit" @click="handleEdit(scope.$index, scope.row)">
							Edit
						</el-button>
						<el-button text :icon="Delete" class="red" @click="handleDelete(scope.$index)">
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
			<el-form label-width="70px">
				<el-form-item label="Username">
					<el-input v-model="form.name"></el-input>
				</el-form-item>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="editVisible = false">Cancel</el-button>
					<el-button type="primary" @click="saveEdit">Confirm</el-button>
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

interface TableItem {
	id: number;
	cloud_platform: string;
	account: string;
	project_name: string;
	status: string;
	create_time: string;
}

const query = reactive({
	name: '',
	pageIndex: 1,
	pageSize: 10
});


const obj = [
	{
		id: 1,
		cloud_platform: "AlibabaCloud",
		account: 'sunway@mtr.onaliyun.com',
		project_name: "mtr",
		status: "Running",
		create_time: "2019-11-1"
	},
	{
		id: 2,
		cloud_platform: "AlibabaCloud",
		account: 'sunway@hci.onaliyun.com',
		project_name: "hci",
		status: "Running",
		create_time: "2019-11-1"
	},
];

const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);

const arr = [];

Object.keys(obj).forEach(v => {
	let o = {};
	o = obj[v];
	arr.push(o)
})

// 获取表格数据
const getData = () => {
	pageTotal.value = obj.length;
	tableData.value = arr;
	const res = sendGetReq({uri: "/project/list"}).then((res) => {
		  console.log("res.data===========",res.data)
		}
	);
};
getData();

// 查询操作
const handleSearch = () => {
	query.pageIndex = 1;
	getData();
};
// 分页导航
const handlePageChange = (val: number) => {
	query.pageIndex = val;
	getData();
};

// 删除操作
const handleDelete = (index: number) => {
	// 二次确认删除
	ElMessageBox.confirm('确定要删除吗？', '提示', {
		type: 'warning'
	})
		.then(() => {
			ElMessage.success('删除成功');
			tableData.value.splice(index, 1);
		})
		.catch(() => {
		});
};

// 表格编辑时弹窗和保存
const editVisible = ref(false);
let form = reactive({
	name: ''
});
let idx: number = -1;
const handleEdit = (index: number, row: any) => {
	idx = index;
	form.name = row.name;
	editVisible.value = true;
};
const saveEdit = () => {
	editVisible.value = false;
	ElMessage.success(`修改第 ${idx + 1} 行成功`);
	tableData.value[idx].project_name = form.name;
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
