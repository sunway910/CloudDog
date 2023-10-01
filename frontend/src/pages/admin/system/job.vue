<!--Advanced Python Scheduler: Job Service-->
<template>
	<div>
		<div class="product_container">
			<div class="handle-box">
				<el-input
					v-model="queryConditions.project_name"
					@keydown.enter="searchJobs"
					:placeholder=t(job_i18n.job_name)
					class="handle-input mr10"
				></el-input>
				<el-button :icon="Search" type="primary" @click="searchJobs"
					>{{ t(base_i18n.search) }}</el-button
				>
				<el-button
					:icon="Refresh"
					type="primary"
					@click="getJobList"
					style="float: right"
					>{{ t(base_i18n.refresh) }}</el-button
				>
			</div>

			<el-scrollbar>
				<el-table
					:data="DjangoAPSchedulerJobList"
					:border="parentBorder"
					header-cell-class-name="table-header"
					scrollbar-always-on
					style="width: 100%"
				>
					<el-table-column
						align="center"
						:label=t(job_i18n.job_name)
						show-overflow-tooltip
						width="300px"
					>
						<template #default="scope">
							<div style="font-weight: bold">
								{{ scope.row.id }}
							</div>
						</template>
					</el-table-column>

					<el-table-column
						align="center"
						:label=t(job_i18n.next_run_time)
						show-overflow-tooltip
						width="500px"
						color:red
					>
						<template #default="scope">
							<div style="font-weight: bold">
								{{ changeTimePattern(scope.row.next_run_time) }}
							</div>
						</template>
					</el-table-column>

					<el-table-column
						prop="job_state"
						:label=t(job_i18n.job_state)
						align="center"
						width="800px"
						show-overflow-tooltip
					>
						<template #default="scope">
							<div style="font-weight: bold">
								{{ scope.row.job_state }}
							</div>
						</template>
					</el-table-column>

					<el-table-column
						:label=t(base_i18n.operation)
						width="220"
						align="center"
						v-if="auth.key.includes(String(role[0]))"
						fixed="right"
					>
						<template #default="scope">
							<el-button
								text
								:icon="Edit"
								@click="handleUpdate(scope.$index, scope.row)"
							>
								Edit
							</el-button>
							<el-button
								text
								:icon="Delete"
								class="red"
								@click="deleteProject(scope.row)"
							>
								Delete
							</el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-scrollbar>

			<div class="admin_pagination">
				<el-pagination
					v-model:current-page="currentPageIndex"
					v-model:page-size="pageSize"
					:page-sizes="[10, 20, 30, 50]"
					:small="small"
					:disabled="disabled"
					:background="background"
					layout="total, sizes, prev, pager, next, jumper"
					:total="pageTotal"
					@size-change="handleSizeChange"
					@current-change="handlePageChange"
				/>
			</div>
		</div>
		<!-- operate job -->
		<el-dialog title="Edit" v-model="DialogVisible" width="40%">
			<el-form label-width="150px" v-model="JobInstance">
				<el-tooltip content="Input Job Name" placement="top">
					<el-form-item label="Job Name" required>
						<el-input
							v-model="JobInstance.id"
							placeholder="Input Job Name"
						></el-input>
					</el-form-item>
				</el-tooltip>
				<el-tooltip content="Input Job Next Run Time" placement="top">
					<el-form-item label="Job Next Run Time" required>
						<el-input
							v-model="JobInstance.next_run_time"
							placeholder="Input Job Next Run Time"
						></el-input>
					</el-form-item>
				</el-tooltip>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="DialogVisible = false">Cancel</el-button>
					<el-button type="primary" @click="operateJob">Confirm</el-button>
				</span>
			</template>
		</el-dialog>
	</div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { Delete, Edit, Refresh, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '~/stores/auth'
import {changeTimePattern, job_i18n, base_i18n} from "~/stores/utils";

const {t} = useI18n()
const auth = useAuthStore()
const parentBorder = ref(true)
const role = ['admin', 'user']
const small = ref(false)
const background = ref(true)
const disabled = ref(false)
const DialogVisible = ref(false) // el-dialog
const createOrUpdateRequest = ref(true) // false means create request, true means update request
// The pattern of Project
interface DjangoAPSchedulerJob {
	id: any
	next_run_time: string
	job_state: string
}

let JobInstance = reactive<DjangoAPSchedulerJob>({
	id: '',
	next_run_time: '',
	job_state: '',
})

const DjangoAPSchedulerJobList = ref<DjangoAPSchedulerJob[]>([])
const pageTotal = ref(0)

// The conditions of search api
const queryConditions = reactive({
	project_name: '',
})

let currentPageIndex = ref(1)
let pageSize = ref(10)

// get Elastic Compute Resource list
const getJobList = () => {
	sendGetReq({
		params: {
			page_index: currentPageIndex.value,
			page_size: pageSize.value,
		},
		uri: '/apsjob',
	})
		.then((res) => {
			pageTotal.value = parseInt(res.data.count)
			DjangoAPSchedulerJobList.value = res.data.results
		})
		.catch((err) => {
			ElMessage.error(err || 'Get job list error')
		})
}
getJobList() // init ECR list

// search ECR by cloud_platform and project_name
const searchJobs = () => {
	sendGetReq({
		uri: '/apsjob',
		params: {
			job_name: queryConditions.project_name,
			page_index: currentPageIndex.value,
			page_size: pageSize.value,
		},
	})
		.then((res) => {
			pageTotal.value = parseInt(res.data.total)
			DjangoAPSchedulerJobList.value = res.data.data
		})
		.catch((err) => {
			ElMessage.error(err || 'Search job error')
		})
}

const handlePageChange = (val: number) => {
	currentPageIndex.value = val
	getJobList()
}

const handleSizeChange = (val: number) => {
	pageSize.value = val
	getJobList()
}

const handleUpdate = (index: number, row: any) => {
	idx = index
	JobInstance = row // init data which should be updated
	DialogVisible.value = true // open dialog page
	createOrUpdateRequest.value = true // set dialog mode to 'update'
}

const deleteProject = (row: any) => {
	ElMessageBox.confirm('Are you sure you want to delete it', 'Message', {
		type: 'warning',
	})
		.then(() => {
			sendDeleteReq({ uri: '/project/delete', params: { id: row.id } })
			ElMessage.success('delete successfully')
		})
		.catch(() => {
			ElMessage.error('delete failed')
		})
	getJobList()
}

const operateJob = () => {
	sendPostReq({ uri: '/apsjob/', payload: JobInstance, config_obj: null }).then(
		() => {
			getJobList() // create operation need to requery project list from db
		},
	)
	DialogVisible.value = false // close dialog page
}
</script>

<style>
.handle-box {
	margin-bottom: 20px;
}

.handle-input {
	width: 300px;
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

.el-popper.is-customized .el-popper__arrow::before {
	background: linear-gradient(45deg, #b2e68d, #bce689);
	right: 0;
}
</style>
