<!--Elastic Compute Service-->
<template>

  <div>
    <div class="product_container">
      <div class="handle-box">
        <el-input v-model="queryConditions.project_name" @keydown.enter="searchEcr" :placeholder=t(base_i18n.project_name) class="handle-input mr10"></el-input>
        <el-button color="#626aef" :icon="Search" type="primary" @click="searchEcr">{{ t(base_i18n.search) }}</el-button>
        <el-button :icon="Refresh" type="primary" @click="getECRList" style="float: right">{{ t(base_i18n.refresh) }}</el-button>
        <el-button type="primary" @click="exportXlsx" style="float: right">{{ t(base_i18n.export) }}</el-button>
      </div>

      <el-scrollbar>
        <el-table :data="elasticComputeResourceList"
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
                <p m="t-0 b-2" style="font-weight: bold">{{ t(ecs_i18n.start_time) }}: {{ changeTimePattern(props.row.start_time) }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(ecs_i18n.stopped_mode) }}: {{ props.row.stopped_mode }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.instance_id) }}: {{ props.row.instance_id }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(ecs_i18n.lock_reason) }}: {{ props.row.lock_reason }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.internet_charge_type) }}: {{ props.row.internet_charge_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.auto_release_time) }}: {{ props.row.auto_release_time ? props.row.auto_release_time : 'None' }}</p>
              </div>
            </template>
          </el-table-column>
          <el-table-column align="center" :label=t(base_i18n.project_name) show-overflow-tooltip width="100px">
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.project_name }}
              </div>
            </template>
          </el-table-column>
          <el-table-column align="center" :label=t(ecs_i18n.instance_name) show-overflow-tooltip width="200px" color:red>
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.instance_name }}
              </div>
            </template>
          </el-table-column>

          <el-table-column :label=t(ecs_i18n.auto_renew_enabled) align="center" width="180px">
            <template #default="scope">
              <el-tag :type="scope.row.auto_renew_enabled ? 'success' : 'danger'">
                {{ scope.row.auto_renew_enabled ? "True" : "False" }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column :label=t(ecs_i18n.ecs_status) align="center" width="100px" :render-header="renderHeader">
            <template #default="scope">
              <el-tag :type="scope.row.ecs_status === 'Running' ? 'success' : 'danger'">
                {{ scope.row.ecs_status }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column align="center" :label=t(base_i18n.region_id) show-overflow-tooltip width="150px" font-weight: bold>
            <template #default="scope" style="font-weight: bold">
              <div style="font-weight: bold">
                {{ scope.row.region_id.toString().split('-')[1].substring(0, 1).toUpperCase() + scope.row.region_id.toString().split('-')[1].substring(1).toLowerCase() }}
              </div>
            </template>
          </el-table-column>

          <el-table-column align="center" :label=t(base_i18n.expired_time) show-overflow-tooltip width="150px">
            <template #default="scope">
              <el-tag>
                {{ scope.row.expired_time.toString().substring(0, 10) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="instance_charge_type" align="center" :label=t(base_i18n.instance_charge_type) show-overflow-tooltip width="180px"
                           :render-header="renderHeader"></el-table-column>
          <el-table-column prop="duration" align="center" :label=t(ecs_i18n.duration) show-overflow-tooltip width="120px"></el-table-column>
          <el-table-column prop="renewal_status" align="center" :label=t(base_i18n.renewal_status) show-overflow-tooltip width="160px"></el-table-column>
          <el-table-column prop="period_init" align="center" :label=t(ecs_i18n.period_init) show-overflow-tooltip width="180px"></el-table-column>


          <el-table-column prop="api_request_id" align="center" :label=t(base_i18n.api_request_id) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column align="center" :label=t(base_i18n.request_time) show-overflow-tooltip width="180px">
            <template #default="scope">
              <el-tag>
                {{ changeTimePattern(scope.row.request_time) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="product_type" align="center" :label=t(base_i18n.product_type) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column prop="start_time" align="center" :label=t(ecs_i18n.start_time) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column prop="stopped_mode" align="center" :label=t(ecs_i18n.stopped_mode) show-overflow-tooltip width="180px" :render-header="renderHeader"></el-table-column>
          <el-table-column prop="instance_id" align="center" :label=t(base_i18n.instance_id) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column prop="internet_charge_type" align="center" :label=t(base_i18n.internet_charge_type) show-overflow-tooltip width="180px" :render-header="renderHeader"></el-table-column>
          <el-table-column prop="lock_reason" align="center" :label=t(ecs_i18n.lock_reason) show-overflow-tooltip width="180px" :render-header="renderHeader"></el-table-column>
          <el-table-column prop="auto_release_time" align="center" :label=t(base_i18n.auto_release_time) show-overflow-tooltip width="210px">
            <template #default="scope">
              {{ scope.row.auto_release_time ? scope.row.auto_release_time : '-' }}
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

  </div>
</template>

<script setup lang="ts">
import {h, reactive, ref} from 'vue';
import {Refresh, Search} from '@element-plus/icons-vue';
import {ElTooltip, ElMessage} from 'element-plus';
import * as XLSX from 'xlsx';
import {changeTimePattern, ecs_i18n, base_i18n} from "~/stores/utils";

const {t} = useI18n()
const parentBorder = ref(true)
const auth = ['admin', 'user']
const small = ref(false)
const background = ref(true)
const disabled = ref(false)

const StatusDescription = ref("" +
    "(Pending, 创建中)--" +
    "(Running, 运行中)--" +
    "(Starting, 启动中)--" +
    "(Stopping, 停止中)--" +
    "(Stopped, 已停止)")

const LockReasonDescription = ref("" +
    "(financial, 因欠费被锁定)" +
    "(security, 因安全原因被锁定)" +
    "(Recycling, 抢占式实例的待释放锁定状态)" +
    "(dedicatedhostfinancial, 因为专有宿主机欠费导致ECS实例被锁定)" +
    "(refunded, 因退款被锁定)")

const InternetChargeTypeDescription = ref("" +
    "(PayByBandwidth, 按固定带宽计费)" +
    "(PayByTraffic, 按使用流量计费)")

const InstanceChargeTypeDescription = ref("" +
    "(PostPaid, 按量付费)--" +
    "(PrePaid, 包年包月)")

const StoppedModeDescription = ref("" +
    "(KeepCharging, 停机后继续收费，为您继续保留库存资源)" +
    "(Not-applicable, 停机后不收费。停机后会释放实例对应的资源，例如vCPU、内存和公网IP等资源)" +
    "(StopCharging, 包年包月)")


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
interface ElasticComputeResource {
  api_request_id: any,
  instance_id: string,
  request_time: string,
  product_type: string,
  project: string,
  instance_name: string,
  auto_renew_enabled: string,
  renewal_status: string,
  period_init: string,
  duration: string,
  region_id: string,
  ecs_status: string,
  instance_charge_type: string,
  internet_charge_type: string,
  expired_time: string,
  stopped_mode: string,
  start_time: string,
  auto_release_time: string,
  lock_reason: string,
}

const excelList = [[
  'api_request_id',
  'instance_id',
  'request_time',
  'product_type',
  'project',
  'instance_name',
  'auto_renew_enabled',
  'renewal_status',
  'period_init',
  'duration',
  'region_id',
  'ecs_status',
  'instance_charge_type',
  'internet_charge_type',
  'expired_time',
  'stopped_mode',
  'start_time',
  'auto_release_time',
  'lock_reason',
]];
const elasticComputeResourceList = ref<ElasticComputeResource[]>([]);
const pageTotal = ref(0);

// The conditions of search api
const queryConditions = reactive({
  project_name: "",
});

let currentPageIndex = ref(1);
let pageSize = ref(10);

const tableRowClassName = ({row}: { row: ElasticComputeResource }) => {
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
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    },
    uri: "/ecs/list"
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        elasticComputeResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get ecr list error');
  });
}
getECRList(); // init ECR list

// search ECR by project_name
const searchEcr = () => {
  sendGetReq({
    uri: "/ecs/search", params: {
      project_name: queryConditions.project_name,
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    }
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        elasticComputeResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Search project error');
  });
}

const handlePageChange = (val: number) => {
  currentPageIndex.value = val;
  getECRList();
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  getECRList();
}

const exportXlsx = () => {
  elasticComputeResourceList.value.map((item: any) => {
    let arr = [];
    arr.push(item.api_request_id, item.instance_id, item.request_time,
        item.product_type, item.project_name, item.instance_name, item.auto_renew_enabled,
        item.renewal_status, item.period_init, item.duration, item.region_id,
        item.ecs_status, item.instance_charge_type, item.internet_charge_type, item.expired_time,
        item.stopped_mode, item.start_time, item.auto_release_time, item.lock_reason
    );
    excelList.push(arr);
  });
  let WorkSheet = XLSX.utils.aoa_to_sheet(excelList);
  let new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, 'ecr');
  XLSX.writeFile(new_workbook, `ecr_summary.xlsx`);
};


const getDescription = (label: string) => {
  switch (label) {
    case "Status":
      return StatusDescription.value;
    case "Lock Reason":
      return LockReasonDescription.value;
    case "Internet Charge Type":
      return InternetChargeTypeDescription.value;
    case "Instance Charge Type":
      return InstanceChargeTypeDescription.value;
    case "Stopped Mode":
      return StoppedModeDescription.value;
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
