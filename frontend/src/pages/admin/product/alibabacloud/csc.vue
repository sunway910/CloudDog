<!--Application Server load balancer-->
<template>
  <div>
    <div class="product_container">
      <div class="handle-box">

        <el-input v-model="queryConditions.project_name" @keydown.enter="getCSCList" :placeholder=t(base_i18n.project_name) class="handle-input mr10"></el-input>
        <el-button color="#626aef" :icon="Search" type="primary" @click="getCSCList">{{ t(base_i18n.search) }}</el-button>
        <el-button :icon="Refresh" type="primary" @click="getCSCList" style="float: right">{{ t(base_i18n.refresh) }}</el-button>
        <el-button type="primary" @click="exportXlsx" style="float: right">{{ t(base_i18n.export) }}</el-button>
      </div>

      <el-scrollbar>
        <el-table :data="cscResourceList"
                  :border="parentBorder"
                  header-cell-class-name="table-header"
                  scrollbar-always-on
                  style="width: 100%">
          <el-table-column type="expand">
            <template #default="props">
              <div m="4">
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.api_request_id) }}: {{ props.row.api_request_id }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.request_time) }}: {{ changeTimePattern(props.row.request_time) }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.product_type) }}: {{ props.row.product_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.product_name) }}: {{ props.row.product_name }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.mv_auth_count) }}: {{ props.row.mv_auth_count }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.sas_log) }}: {{ props.row.sas_log }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.sas_screen) }}: {{ props.row.sas_screen }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.honeypot_capacity) }}: {{ props.row.honeypot_capacity }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.mv_unused_auth_count) }}: {{ props.row.mv_unused_auth_count }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.web_lock) }}: {{ props.row.web_lock }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.app_white_list_auth_count) }}: {{ props.row.app_white_list_auth_count }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.last_trail_end_time) }}: {{ props.row.last_trail_end_time }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.version) }}: {{ props.row.version }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.web_lock_auth_count) }}: {{ props.row.web_lock_auth_count }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.release_time) }}: {{ props.row.release_time }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.highest_version) }}: {{ props.row.highest_version }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.asset_level) }}: {{ props.row.asset_level }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.is_over_balance) }}: {{ props.row.is_over_balance }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.sls_capacity) }}: {{ props.row.sls_capacity }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.vm_cores) }}: {{ props.row.vm_cores }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.allow_partial_buy) }}: {{ props.row.allow_partial_buy }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.app_white_list) }}: {{ props.row.app_white_list }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.image_scan_capacity) }}: {{ props.row.image_scan_capacity }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.is_trial_version) }}: {{ props.row.is_trial_version }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.user_defined_alarms) }}: {{ props.row.user_defined_alarms }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.open_time) }}: {{ props.row.open_time }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.is_new_container_version) }}: {{ props.row.is_new_container_version }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.is_new_multi_version) }}: {{ props.row.is_new_multi_version }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.threat_analysis_capacity) }}: {{ props.row.threat_analysis_capacity }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.cspm_capacity) }}: {{ props.row.cspm_capacity }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.vul_fix_capacity) }}: {{ props.row.vul_fix_capacity }}</p>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(csc_i18n.rasp_capacity) }}: {{ props.row.rasp_capacity }}</p>
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
          <el-table-column prop="mv_auth_count" align="center" :label=t(csc_i18n.mv_auth_count) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column :render-header="renderHeader" prop="sas_log" align="center" :label=t(csc_i18n.sas_log) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column :render-header="renderHeader" prop="sas_screen" align="center" :label=t(csc_i18n.sas_screen) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="mv_unused_auth_count" align="center" :label=t(csc_i18n.mv_unused_auth_count) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column :render-header="renderHeader" prop="web_lock" align="center" :label=t(csc_i18n.web_lock) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="app_white_list_auth_count" align="center" :label=t(csc_i18n.app_white_list_auth_count) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="last_trail_end_time" align="center" :label=t(csc_i18n.last_trail_end_time) show-overflow-tooltip width="150px">
            <template #default="scope">
              <el-tag>
                {{ changeTimePattern(scope.row.last_trail_end_time) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column :render-header="renderHeader" prop="version" align="center" :label=t(csc_i18n.version) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="web_lock_auth_count" align="center" :label=t(csc_i18n.web_lock_auth_count) show-overflow-tooltip width="165px"></el-table-column>
          <el-table-column prop="release_time" align="center" :label=t(csc_i18n.release_time) show-overflow-tooltip width="180px">
            <template #default="scope">
              <el-tag>
                {{ changeTimePattern(scope.row.release_time) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column :render-header="renderHeader" prop="highest_version" align="center" :label=t(csc_i18n.highest_version) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column align="center" prop="asset_level" :label=t(csc_i18n.asset_level) show-overflow-tooltip width="250px" font-weight: bold></el-table-column>
          <el-table-column prop="is_over_balance" :label=t(csc_i18n.is_over_balance) align="center" width="180px"></el-table-column>
          <el-table-column prop="sls_capacity" :label=t(csc_i18n.sls_capacity) align="center" width="180px"></el-table-column>
          <el-table-column prop="vm_cores" :label=t(csc_i18n.vm_cores) align="center" width="180px"></el-table-column>
          <el-table-column prop="allow_partial_buy" :label=t(csc_i18n.allow_partial_buy) align="center" width="180px"></el-table-column>
          <el-table-column prop="app_white_list" :label=t(csc_i18n.app_white_list) align="center" width="180px"></el-table-column>
          <el-table-column prop="image_scan_capacity" :label=t(csc_i18n.image_scan_capacity) align="center" width="180px"></el-table-column>
          <el-table-column prop="is_trial_version" :label=t(csc_i18n.is_trial_version) align="center" width="180px"></el-table-column>
          <el-table-column prop="user_defined_alarms" :label=t(csc_i18n.user_defined_alarms) align="center" width="180px"></el-table-column>
          <el-table-column :label=t(csc_i18n.open_time) align="center" width="180px">
            <template #default="scope">
              <el-tag>
                {{ changeTimePattern(scope.row.open_time) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="is_new_container_version" :label=t(csc_i18n.is_new_container_version) align="center" width="180px"></el-table-column>
          <el-table-column prop="is_new_multi_version" :label=t(csc_i18n.is_new_multi_version) align="center" width="180px"></el-table-column>
          <el-table-column prop="threat_analysis_capacity" :label=t(csc_i18n.threat_analysis_capacity) align="center" width="180px"></el-table-column>
          <el-table-column prop="cspm_capacity" :label=t(csc_i18n.cspm_capacity) align="center" width="180px"></el-table-column>
          <el-table-column prop="vul_fix_capacity" :label=t(csc_i18n.vul_fix_capacity) align="center" width="180px"></el-table-column>
          <el-table-column prop="rasp_capacity" :label=t(csc_i18n.rasp_capacity) align="center" width="180px"></el-table-column>
          <el-table-column prop="api_request_id" align="center" :label=t(base_i18n.api_request_id) show-overflow-tooltip width="180px">

          </el-table-column>
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
import {changeTimePattern, csc_i18n, base_i18n} from "~/stores/utils";

const {t} = useI18n()
const parentBorder = ref(true)
const auth = ['admin', 'user']
const small = ref(false)
const background = ref(true)
const disabled = ref(false)

const Status = ref("" +
    "(0, 未购买)--" +
    " (1, 已购买)")
const IsEnabled = ref("" +
    "(0, 未开启)--" +
    " (1, 已开启)")
const Version = ref("" +
    "(1, 免费版)--" +
    " (3, 企业版)--" +
    " (5, 高级版)--" +
    " (6, 防病毒版)--" +
    " (7, 旗舰版)--" +
    " (8, 多版本)--" +
    " (10, 仅采购增值服务)--")
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
interface cscResource {
  api_request_id: any,
  instance_id: string,
  request_time: string,
  product_type: string,
  project_name: string,
  mv_auth_count: any,
  sas_log: any,
  sas_screen: any,
  honeypot_capacity: any,
  mv_unused_auth_count: any,
  web_lock: any,
  app_white_list_auth_count: any,
  last_trail_end_time: any,
  version: any,
  web_lock_auth_count: any,
  release_time: any,
  highest_version: any,
  asset_level: any,
  is_over_balance: any,
  sls_capacity: any,
  vm_cores: any,
  allow_partial_buy: any,
  app_white_list: any,
  image_scan_capacity: any,
  is_trial_version: any,
  user_defined_alarms: any,
  open_time: any,
  is_new_container_version: any,
  is_new_multi_version: any,
  threat_analysis_capacity: any,
  cspm_capacity: any,
  vul_fix_capacity: any,
  rasp_capacity: any,
}

const excelList = [[
  'api_request_id',
  'instance_id',
  'request_time',
  'product_type',
  'project_name',
  'mv_auth_count',
  'sas_log',
  'sas_screen',
  'honeypot_capacity',
  'mv_unused_auth_count',
  'web_lock',
  'app_white_list_auth_count',
  'last_trail_end_time',
  'version',
  'web_lock_auth_count',
  'release_time',
  'highest_version',
  'asset_level',
  'is_over_balance',
  'sls_capacity',
  'vm_cores',
  'allow_partial_buy',
  'app_white_list',
  'image_scan_capacity',
  'is_trial_version',
  'user_defined_alarms',
  'open_time',
  'is_new_container_version',
  'is_new_multi_version',
  'threat_analysis_capacity',
  'cspm_capacity',
  'vul_fix_capacity',
  'rasp_capacity',
]];
const cscResourceList = ref<cscResource[]>([]);
const pageTotal = ref(0);

// The conditions of search api
const queryConditions = reactive({
  project_name: "",
});

let currentPageIndex = ref(1);
let pageSize = ref(10);

const getCSCList = () => {
  sendGetReq({
    params: {
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    },
    uri: "/csc/list"
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        cscResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get csc list error');
  });
}
getCSCList()

const handlePageChange = (val: number) => {
  currentPageIndex.value = val;
  getCSCList();
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  getCSCList();
}
const exportXlsx = () => {
  cscResourceList.value.map((item: any) => {
    let arr = [];
    arr.push(item.api_request_id, item.instance_id, item.request_time,
        item.product_type, item.project_name,
        item.mv_auth_count, item.sas_log, item.sas_screen,
        item.honeypot_capacity, item.mv_unused_auth_count, item.web_lock, item.app_white_list_auth_count,
        item.last_trail_end_time, item.version,
        item.web_lock_auth_count, item.release_time, item.highest_version, item.asset_level,
        item.is_over_balance, item.sls_capacity, item.vm_cores, item.allow_partial_buy,
        item.app_white_list, item.image_scan_capacity, item.is_trial_version,
        item.user_defined_alarms, item.open_time, item.is_new_container_version,
        item.is_new_multi_version, item.threat_analysis_capacity, item.cspm_capacity,
        item.vul_fix_capacity, item.rasp_capacity,
    );
    excelList.push(arr);
  });
  let WorkSheet = XLSX.utils.aoa_to_sheet(excelList);
  let new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, 'csc');
  XLSX.writeFile(new_workbook, `csc_summary.xlsx`);
};

const getDescription = (label: string) => {
  switch (label) {
    case "Status":
      return Status.value;
    case "IsEnabled":
      return IsEnabled.value;
    case "Version":
      return Version.value;
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
