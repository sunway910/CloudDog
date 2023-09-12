<!--Elastic Compute Service-->
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
				<el-button :icon="Refresh" type="primary" @click="getECRList" style="float: right">Refresh</el-button>
			</div>

			<el-scrollbar>
				<el-table :data="elasticComputeResourceList.slice((pageIndex - 1) * pageSize, pageIndex * pageSize)"
									border
									header-cell-class-name="table-header"
									:row-class-name="tableRowClassName"
									scrollbar-always-on
									style="width: 100%">
					<el-table-column prop="api_request_id" align="center" label="Request Id" width="100px" show-overflow-tooltip></el-table-column>
					<el-table-column align="center" label="Project" show-overflow-tooltip width="100px">
						<template #default="scope">
							<div style="font-weight: bold">
								{{ scope.row.project_name }}
							</div>
						</template>
					</el-table-column>
					<el-table-column align="center" label="Name" show-overflow-tooltip width="200px" color:red>
						<template #default="scope">
							<div style="font-weight: bold">
								{{ scope.row.instance_name }}
							</div>
						</template>
					</el-table-column>
					<el-table-column label="Auto Renew Enabled" align="center" width="165px">
						<template #default="scope">
							<el-tag :type="scope.row.auto_renew_enabled ? 'success' : 'danger'">
								{{ scope.row.auto_renew_enabled ? "True" : "False" }}
							</el-tag>
						</template>
					</el-table-column>
					<el-table-column label="Status" align="center" width="100px">
						<template #default="scope">
							<el-tag :type="scope.row.ecs_status === 'Running' ? 'success' : 'danger'">
								{{ scope.row.ecs_status }}
							</el-tag>
						</template>
					</el-table-column>
					<el-table-column align="center" label="Region" show-overflow-tooltip width="150px" font-weight: bold>
						<template #default="scope" style="font-weight: bold">
							<div style="font-weight: bold">
								{{ scope.row.region_id.toString().split('-')[1].substring(0, 1).toUpperCase() + scope.row.region_id.toString().split('-')[1].substring(1).toLowerCase() }}
							</div>
						</template>
					</el-table-column>
					<el-table-column prop="expired_time" align="center" label="Expired Time" show-overflow-tooltip width="150px">
						<template #default="scope">
							<el-tag>
								{{ scope.row.expired_time.toString().substring(0, 10) }}
							</el-tag>
						</template>
					</el-table-column>
					<el-table-column prop="instance_charge_type" align="center" label="Instance Charge Type" show-overflow-tooltip width="180px"></el-table-column>
					<el-table-column prop="duration" align="center" label="Renewal Time" show-overflow-tooltip width="120px"></el-table-column>
					<el-table-column prop="renewal_status" align="center" label="Renewal Status" show-overflow-tooltip width="130px"></el-table-column>
					<el-table-column prop="period_init" align="center" label="Renewal Period Unit" show-overflow-tooltip width="180px"></el-table-column>
					<el-table-column prop="request_time" align="center" label="Request Time" show-overflow-tooltip width="150px"></el-table-column>
					<el-table-column prop="product_type" align="center" label="Type" width="80px"></el-table-column>
					<el-table-column prop="internet_charge_type" align="center" label="Internet Charge Type" show-overflow-tooltip width="180px"></el-table-column>
					<el-table-column prop="stopped_mode" align="center" label="Stopped Mode" show-overflow-tooltip width="140px"></el-table-column>
					<el-table-column prop="start_time" align="center" label="Instance Start Time" show-overflow-tooltip width="160px"></el-table-column>
					<el-table-column prop="instance_id" align="center" label="Instance ID" width="150px" show-overflow-tooltip></el-table-column>
					<el-table-column prop="lock_reason" align="center" label="Lock Reason" show-overflow-tooltip width="120px"></el-table-column>
					<el-table-column prop="auto_release_time" align="center" label="Auto Release Time" show-overflow-tooltip width="180px">
						<template #default="scope">
							<el-tag>
								{{ scope.row.auto_release_time ? scope.row.auto_release_time : '-' }}
							</el-tag>
						</template>
					</el-table-column>

				</el-table>
			</el-scrollbar>

			<div class="admin_pagination">
				<el-pagination
					background
					layout="total, prev, pager, next"
					:current-page="pageIndex"
					:page-size="pageSize"
					:total="pageTotal"
					@current-change="handlePageChange"
				></el-pagination>
			</div>
		</div>

	</div>
</template>

<script setup lang="ts">
import {ref, reactive} from 'vue';
import {ElMessage} from 'element-plus';
import {Search, Refresh} from '@element-plus/icons-vue';
import router from "@/plugins/router";

const auth = ['admin', 'user']

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
interface ElasticComputeResource {
	api_request_id: any;
	instance_id: string;
	request_time: string;
	product_type: string;
	project: string,
	instance_name: string,
	auto_renew_enabled: string,
	renewal_status: string;
	period_init: string;
	duration: string;
	region_id: string;
	ecs_status: string;
	instance_charge_type: string;
	internet_charge_type: string;
	expired_time: string;
	stopped_mode: string;
	start_time: string;
	auto_release_time: string;
	lock_reason: string;
}

const elasticComputeResourceList = ref<ElasticComputeResource[]>([]);
const pageTotal = ref(0);

// The conditions of search api
const queryConditions = reactive({
	cloud_platform: "",
	project_name: "",
});
let pageIndex = 1, pageSize = 20;
const tableRowClassName = ({row}: {
	row: ElasticComputeResource
}) => {
	if (row.ecs_status === 'Running') {
		return 'success-row'
	} else {
		return 'warning-row'
	}
}


// get Elastic Compute Resource list
const getECRList = () => {
	sendGetReq({
		params: {
			page_index: pageIndex,
			page_size: pageSize
		},
		uri: "/ecs/list"
	}).then((res) => {
			pageTotal.value = parseInt(res.data.data.length)
			elasticComputeResourceList.value = res.data.data
		}
	).catch((err) => {
		ElMessage.error(err || 'Get ecr list error');
	});
}
getECRList(); // init ECR list

// search ECR by cloud_platform and project_name
const searchProjects = () => {
	sendGetReq({uri: "/ecs/search", params: {cloud_platform: queryConditions.cloud_platform, project_name: queryConditions.project_name}}).then((res) => {
			pageTotal.value = parseInt(res.data.data.length)
			elasticComputeResourceList.value = res.data.data
		}
	).catch((err) => {
		ElMessage.error(err || 'Search project error');
	});
}


const handlePageChange = (val: number) => {
	console.log("row==", val)
	pageIndex = val;
	getECRList();
};


</script>

<style>
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
	display: flex;
	width: 100%;
	font-size: 14px;
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

.el-scrollbar__bar.is-horizontal {
	height: 15px !important;
}

.el-table .warning-row {
	--el-table-tr-bg-color: var(--el-color-warning-light-9);
}

.el-table .success-row {
	--el-table-tr-bg-color: var(--el-color-success-light-9);
}

</style>
