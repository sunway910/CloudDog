<template>
  <div>
    <div class="product_container">
      <div class="handle-box">
        <el-select v-model="queryConditions.platform" placeholder="Cloud Platform" class="handle-select mr10">
          <el-option
              v-for="item in platformOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
        <el-input v-model="queryConditions.project_name" @keydown.enter="searchProjects" placeholder="Project Name" class="handle-input mr10"></el-input>
        <el-button :icon="Search" type="primary" @click="searchProjects">Search</el-button>
        <el-button :icon="Plus" type="primary" @click="handleCreate" v-auth=role[0] style="float: right">New</el-button>
        <el-button :icon="Refresh" type="primary" @click="getProjectList" style="float: right">Refresh</el-button>
        <el-button type="primary" @click="exportXlsx" style="float: right">Export</el-button>
      </div>
      <el-scrollbar>
        <el-table :data="projectList"
                  class="table"
                  header-cell-class-name="table-header"
                  :border="parentBorder">
          <el-table-column type="expand">
            <template #default="props">
              <div m="4">
                <p m="t-0 b-2" style="font-weight: bold">Project ID: {{ props.row.id }}</p>
                <p m="t-0 b-2" style="font-weight: bold">Cron Expression: {{ props.row.cron_expression }}</p>
                <p m="t-0 b-2" style="font-weight: bold">RAM Account: {{ props.row.account }}</p>
              </div>
            </template>
          </el-table-column>
          <!--					<el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>-->
          <el-table-column align="center" label="Cloud Platform">
            <template #default="scope">
              <div style="font-weight: bold;color: red">
                <a class="inline-flex items-center gap-2 rounded-lg px-3 py-2"
                   @click="getLoginUrl(scope.row.cloud_platform)"
                   :href="platform_ram_login_url"
                   target="_blank">
                  {{ scope.row.cloud_platform }}
                </a>
              </div>
            </template>
          </el-table-column>
          <el-table-column align="center" label="Project Name" show-overflow-tooltip>
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.project_name }}
              </div>
            </template>
          </el-table-column>
          <el-table-column align="center" label="Region" :formatter="regionFormatter"></el-table-column>
          <el-table-column align="center" label="Toggle">
            <template #default="scope">
              <el-tag :type="scope.row.cron_toggle  ? 'success' : 'danger'">
                {{ scope.row.cron_toggle ? "On" : "Off" }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="Status" align="center">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'Running' ? 'success' : scope.row.status === 'Stopped' ? 'danger' : ''">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="create_time" label="Create Time" align="center" sortable></el-table-column>

          <el-table-column label="Operation" width="220" align="center" v-if="auth.key.includes(String(role[0]))" fixed="right">
            <template #default="scope">
              <el-button text :icon="Edit" @click="handleUpdate(scope.$index,scope.row)">
                Edit
              </el-button>
              <el-button text :icon="Delete" class="red" @click="deleteProject(scope.row)">
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
            :total=pageTotal
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- create or update project -->
    <el-dialog title="Edit" v-model="DialogVisible" width="40%">
      <el-form label-width="150px" v-model="createOrUpdateData">
        <el-form-item label="Cloud Platform">
          <el-select v-model="createOrUpdateData.platform" placeholder="Cloud Platform" class="handle-select mr10" :disabled="createOrUpdateRequest">
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
            <el-input v-model="createOrUpdateData.platform" placeholder="multi region must split with blank"></el-input>
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
        <el-form-item label="Cron Expression" required v-show="!createOrUpdateRequest">
          <el-input v-model="createOrUpdateData.cron_expression" placeholder="Please input crontab"></el-input>
        </el-form-item>
        <el-form-item label="Cron Toggle" required v-show="!createOrUpdateRequest">
          <el-input v-model="createOrUpdateData.cron_toggle" placeholder="Cron Toggle"></el-input>
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
import {useAuthStore} from "~/stores/auth";
import * as https from "https";
import User from "~/pages/admin/auth/user.vue";
import type {TableColumnCtx} from 'element-plus'
import * as XLSX from "xlsx";

const platform_ram_login_url = ref("")
const parentBorder = ref(true)
const small = ref(false)
const background = ref(true)
const disabled = ref(false)
const auth = useAuthStore();
const role = ['admin', 'user']
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
  region: any;
  account: any;
  cloud_platform: string,
  project_access_key: any,
  project_secret_key: any,
  project_name: string;
  cron_expression: any;
  cron_toggle: boolean;
  status: string;
  create_time: string;
}

const projectList = ref<ProjectItem[]>([]);
const pageTotal = ref(0);

const regionFormatter = (row: ProjectItem, column: TableColumnCtx<ProjectItem>) => {
  return row.region.toString().split('-')[1].substring(0, 1).toUpperCase() + row.region.toString().split('-')[1].substring(1).toLowerCase()
}

// The conditions of search api
const queryConditions = reactive({
  cloud_platform: "",
  project_name: "",
});
let currentPageIndex = ref(1);
let pageSize = ref(10);
const DialogVisible = ref(false); // el-dialog
const createOrUpdateRequest = ref(true);  // false means create request, true means update request
let idx: number = -1;

// create or update project
let createOrUpdateData = reactive<ProjectItem>({
  id: -1,
  region: "",
  cloud_platform: "",
  project_name: "",
  project_access_key: null,
  project_secret_key: null,
  cron_expression: "",
  cron_toggle: true,
  account: "",
  status: "",
  create_time: ""
});
const excelList = [[
  'id',
  'region',
  'platform',
  'project_name',
  'cron_expression',
  'cron_toggle',
  'account',
  'status',
  'create_time',
]];
// get project list
const getProjectList = () => {
  sendGetReq({
    uri: "/project/list",
    params: {
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    }
  }).then((res) => {
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
  sendGetReq({
    uri: "/project/search",
    params: {
      page_index: currentPageIndex.value,
      page_size: pageSize.value,
      cloud_platform: queryConditions.cloud_platform,
      project_name: queryConditions.project_name
    }
  }).then((res) => {
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
  currentPageIndex.value = val;
  getProjectList();
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  getProjectList();
}

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
const exportXlsx = () => {
  projectList.value.map((item: any) => {
    let arr = [];
    arr.push(item.id, item.region, item.cloud_platform,
        item.project_name, item.cron_expression, item.cron_toggle,
        item.account, item.status, item.create_time
    );
    excelList.push(arr);
  });
  let WorkSheet = XLSX.utils.aoa_to_sheet(excelList);
  let new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, 'project');
  XLSX.writeFile(new_workbook, `project_summary.xlsx`);
};
const getLoginUrl = (platform: string) => {
  if (platform === 'Aliyun') {
    platform_ram_login_url.value = "https://signin.aliyun.com/login.htm#/main"
  } else if (platform === 'AlibabaCloud') {
    platform_ram_login_url.value = "https://signin.alibabacloud.com/login.htm#/main"
  } else if (platform === 'GCP') {
    platform_ram_login_url.value = "https://console.cloud.google.com/"
  } else if (platform === 'Azure') {
    platform_ram_login_url.value = "https://portal.azure.com/#home"
  } else if (platform === 'AWS') {
    platform_ram_login_url.value = "https://signin.aws.amazon.com/"
  }
};

</script>

<style>

.el-scrollbar__bar.is-horizontal {
  height: 15px !important;
}

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
