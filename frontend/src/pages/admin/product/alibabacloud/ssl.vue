<!--Application Server load balancer-->
<template>
  <div>
    <div class="product_container">
      <div class="handle-box">
        <el-input v-model="queryConditions.project_name" @keydown.enter="searchSSL" :placeholder=t(base_i18n.project_name) class="handle-input mr10"></el-input>
        <el-button color="#626aef" :icon="Search" type="primary" @click="searchSSL">{{ t(base_i18n.search) }}</el-button>
        <el-button :icon="Refresh" type="primary" @click="getSSLList" style="float: right">{{ t(base_i18n.refresh) }}</el-button>
        <el-button type="primary" @click="exportXlsx" style="float: right">{{ t(base_i18n.export) }}</el-button>
      </div>
      <el-scrollbar>
        <el-table :data="sslResourceList"
                  :border="parentBorder"
                  header-cell-class-name="table-header"
                  :row-class-name="tableRowClassName"
                  scrollbar-always-on
                  style="width: 100%">
          <el-table-column type="expand">
            <template #default="props">
              <div m="4">
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.api_request_id) }}: {{ props.row.api_request_id }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.request_time) }}: {{ changeTimePattern(props.row.request_time) }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.product_type) }}: {{ props.row.product_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.instance_id) }}: {{ props.row.instance_id }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.project_name) }}: {{ props.row.project_name }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.status) }}: {{ props.row.status }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(ssl_i18n.subject_dn) }}: {{ props.row.subject_dn }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(ssl_i18n.common_name) }}: {{ props.row.common_name }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(ssl_i18n.organization_unit) }}: {{ props.row.organization_unit }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(ssl_i18n.organization) }}: {{ props.row.organization }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(ssl_i18n.before_date) }}: {{ props.row.before_date }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(ssl_i18n.after_date) }}: {{ props.row.after_date }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(ssl_i18n.days) }}: {{ props.row.days }}</p><br>

              </div>
            </template>
          </el-table-column>
          <el-table-column align="center" :label=t(base_i18n.project_name) show-overflow-tooltip width="150px">
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.project_name }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="subject_dn" align="center" :label=t(ssl_i18n.subject_dn) show-overflow-tooltip width="250px" font-weight: bold></el-table-column>
          <el-table-column prop="common_name" align="center" :label=t(ssl_i18n.common_name) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="organization_unit" align="center" :label=t(ssl_i18n.organization_unit) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="organization" align="center" :label=t(ssl_i18n.organization) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="before_date" align="center" :label=t(ssl_i18n.before_date) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="after_date" align="center" :label=t(ssl_i18n.after_date) show-overflow-tooltip width="165px"></el-table-column>
          <el-table-column prop="days" align="center" :label=t(ssl_i18n.days) show-overflow-tooltip width="150px"></el-table-column>

          <el-table-column :render-header="renderHeader" align="center" :label=t(base_i18n.status) show-overflow-tooltip width="200px" color:red>
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.status }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="charge_type" align="center" :label=t(base_i18n.instance_charge_type) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column prop="api_request_id" align="center" :label=t(base_i18n.api_request_id) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column align="center" :label=t(base_i18n.request_time) show-overflow-tooltip width="180px">
            <template #default="scope">
              <el-tag>
                {{ changeTimePattern(scope.row.request_time) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="instance_id" align="center" :label=t(base_i18n.instance_id) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column prop="product_type" align="center" :label=t(base_i18n.product_type) show-overflow-tooltip width="180px"></el-table-column>
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

  </div>
</template>

<script setup lang="ts">
import {h, reactive, ref} from 'vue';
import {Refresh, Search} from '@element-plus/icons-vue';
import {ElTooltip, ElMessage} from 'element-plus';
import * as XLSX from 'xlsx';
import {changeTimePattern, ssl_i18n, base_i18n, ecs_i18n} from "@/stores/utils";

const {t} = useI18n()
const parentBorder = ref(true)
const auth = ['admin', 'user']
const small = ref(false)
const background = ref(true)
const disabled = ref(false)


const Status = ref("" +
    "(ISSUE, 正常签发)--" +
    " (REVOKE, 已被吊销)")



const renderHeader = ({column}) => {
  return h('span', {}, [
    h(ElTooltip, {
          effect: 'dark',
          content: getDescription(column.label),
          placement: 'top'
        },
        {default: () => column.label}
    )
  ])
}

// The pattern of Project
interface sslResource {
  api_request_id: any,
  instance_id: string,
  request_time: string,
  product_type: string,
  product_name: string,
  subject_dn: string,
  common_name: string,
  organization_unit: string,
  organization: string,
  status: string,
  before_date: any,
  after_date: any,
  days: any,
}

const excelList = [[
  'api_request_id',
  'instance_id',
  'request_time',
  'product_type',
  'product_name',
  'subject_dn',
  'common_name',
  'organization_unit',
  'organization',
  'status',
  'before_date',
  'after_date',
  'days',
]];
const sslResourceList = ref<sslResource[]>([]);
const pageTotal = ref(0);

// The conditions of search api
const queryConditions = reactive({
  project_name: "",
});

let currentPageIndex = ref(1);
let pageSize = ref(10);

const tableRowClassName = ({row}: { row: sslResource }) => {
  if (row.status === 'ISSUE') {
    return 'success-row'
  } else {
    return 'warning-row'
  }
}


// get Elastic Compute Resource list
const getSSLList = () => {
  sendGetReq({
    params: {
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    },
    uri: "/ssl/list"
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        sslResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get ssl list error');
  });
}
getSSLList(); // init ECR list

// search ECR by project_name
const searchSSL = () => {
  sendGetReq({
    uri: "/ssl/search", params: {
      project_name: queryConditions.project_name,
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    }
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        sslResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Search ssl error');
  });
}

const handlePageChange = (val: number) => {
  currentPageIndex.value = val;
  getSSLList();
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  getSSLList();
}
const exportXlsx = () => {
  sslResourceList.value.map((item: any) => {
    let arr = [];
    arr.push(item.api_request_id, item.instance_id, item.request_time,
        item.product_type, item.project_name,
        item.subject_dn, item.common_name, item.organization_unit,
        item.organization, item.status, item.before_date, item.after_date, item.days,
    );
    excelList.push(arr);
  });
  let WorkSheet = XLSX.utils.aoa_to_sheet(excelList);
  let new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, 'ssl');
  XLSX.writeFile(new_workbook, `ssl_summary.xlsx`);
};

const getDescription = (label: string) => {
  switch (label) {
    case "Status":
      return Status.value;
    default:
      return "-";
  }
}

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

.el-popper.is-customized {
  /* Set padding to ensure the height is 32px */
  padding: 6px 12px;
  background: linear-gradient(90deg, rgb(255, 255, 255), rgb(255, 255, 255));
}

.el-popper.is-customized .el-popper__arrow::before {
  background: linear-gradient(45deg, #b2e68d, #bce689);
  right: 0;
}
</style>
