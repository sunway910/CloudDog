<!--Application Server load balancer-->
<template>
  <div>
    <div class="product_container">
      <div class="handle-box">
        <el-input v-model="queryConditions.project_name" @keydown.enter="searchEip" :placeholder=t(base_i18n.project_name) class="handle-input mr10"></el-input>
        <el-button color="#626aef" :icon="Search" type="primary" @click="searchEip">{{ t(base_i18n.search) }}</el-button>
        <el-button :icon="Refresh" type="primary" @click="getEIPList" style="float: right">{{ t(base_i18n.refresh) }}</el-button>
        <el-button type="primary" @click="exportXlsx" style="float: right">{{ t(base_i18n.export) }}</el-button>
      </div>
      <el-scrollbar>
        <el-table :data="eipResourceList"
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
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.name) }}: {{ props.row.name }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.region_id) }}: {{ props.row.region_id }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.expired_time) }}: {{ props.row.expired_time }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(eip_i18n.allocation_id) }}: {{ props.row.allocation_id }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(eip_i18n.instance_type) }}: {{ props.row.instance_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.internet_charge_type) }}: {{ props.row.internet_charge_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(eip_i18n.business_status) }}: {{ props.row.business_status }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(eip_i18n.reservation_bandwidth) }}: {{ props.row.reservation_bandwidth }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.bandwidth) }}: {{ props.row.bandwidth }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(eip_i18n.ip_address) }}: {{ props.row.ip_address }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(eip_i18n.reservation_internet_charge_type) }}: {{ props.row.reservation_internet_charge_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(eip_i18n.charge_type) }}: {{ props.row.charge_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(eip_i18n.net_mode) }}: {{ props.row.net_mode }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(eip_i18n.allocation_time) }}: {{ props.row.allocation_time }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.status) }}: {{ props.row.status }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(eip_i18n.reservation_active_time) }}: {{ props.row.reservation_active_time }}</p><br>
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
          <el-table-column align="center" :label=t(eip_i18n.allocation_time) show-overflow-tooltip width="250px" font-weight: bold>
            <template #default="scope">
              <div style="font-weight: bold">
                {{ changeTimePattern(scope.row.allocation_time) }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="name" align="center" :label=t(base_i18n.name) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="expired_time" align="center" :label=t(base_i18n.expired_time) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="allocation_id" align="center" :label=t(eip_i18n.allocation_id) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="instance_type" align="center" :label=t(eip_i18n.instance_type) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="internet_charge_type" align="center" :label=t(base_i18n.internet_charge_type) show-overflow-tooltip width="165px"></el-table-column>
          <el-table-column prop="business_status" align="center" :label=t(eip_i18n.business_status) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="reservation_bandwidth" align="center" :label=t(eip_i18n.reservation_bandwidth) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column :render-header="renderHeader" prop="bandwidth" align="center" :label=t(base_i18n.bandwidth) show-overflow-tooltip width="165px"></el-table-column>
          <el-table-column :render-header="renderHeader" prop="ip_address" align="center" :label=t(eip_i18n.ip_address) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column prop="reservation_internet_charge_type" align="center" :label=t(eip_i18n.reservation_internet_charge_type) show-overflow-tooltip width="280px"></el-table-column>
          <el-table-column align="center" prop="charge_type" :label=t(eip_i18n.charge_type) show-overflow-tooltip width="250px" font-weight: bold></el-table-column>
          <el-table-column :render-header="renderHeader" prop="net_mode" :label=t(eip_i18n.net_mode) align="center" width="180px"></el-table-column>
          <el-table-column :render-header="renderHeader" prop="reservation_active_time" :label=t(eip_i18n.reservation_active_time) align="center" width="180px"></el-table-column>
          <el-table-column :render-header="renderHeader" align="center" :label=t(base_i18n.status) show-overflow-tooltip width="200px" color:red>
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.status }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="region_id" :label=t(base_i18n.region_id) align="center" width="100px" show-overflow-tooltip></el-table-column>
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
import {changeTimePattern, eip_i18n, base_i18n, ecs_i18n} from "@/stores/utils";

const {t} = useI18n()
const parentBorder = ref(true)
const auth = ['admin', 'user']
const small = ref(false)
const background = ref(true)
const disabled = ref(false)



const EIPStatus = ref("" +
    "(Associating, 绑定中)--" +
    " (Unassociating, 解绑中)--" +
    " (InUse, 已分配)--" +
    " (Available, 可用)--" +
    " (Releasing, 释放中)")

const ChargeType = ref("" +
    "(PostPaid, 按量计费)" +
    " (PrePaid, 包年包月)")

const BusinessStatus = ref("" +
    "(Normal, 正常)--" +
    " (FinancialLocked, 被锁定)")

const ReservationInternetChargeType = ref("" +
    "(PayByBandwidth, 按固定带宽计费)" +
    " (PayByTraffic, 按使用流量计费)")


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
interface eipResource {
  api_request_id: any,
  instance_id: string,
  request_time: string,
  product_type: string,
  project_name: string,
  name: string,
  region_id: string,
  expired_time: string,
  allocation_id: string,
  instance_type: string,
  internet_charge_type: string,
  business_status: string,
  reservation_bandwidth: string,
  bandwidth: string,
  ip_address: string,
  reservation_internet_charge_type: string,
  charge_type: string,
  net_mode: string,
  allocation_time: string,
  status: string,
  reservation_active_time: string,
}

const excelList = [[
  'api_request_id',
  'instance_id',
  'request_time',
  'product_type',
  'project_name',
  'name',
  'region_id',
  'expired_time',
  'allocation_id',
  'instance_type',
  'internet_charge_type',
  'business_status',
  'reservation_bandwidth',
  'bandwidth',
  'ip_address',
  'reservation_internet_charge_type',
  'charge_type',
  'net_mode',
  'allocation_time',
  'status',
  'reservation_active_time'
]];
const eipResourceList = ref<eipResource[]>([]);
const pageTotal = ref(0);

// The conditions of search api
const queryConditions = reactive({
  project_name: "",
});

let currentPageIndex = ref(1);
let pageSize = ref(10);

const tableRowClassName = ({row}: { row: eipResource }) => {
  if (row.business_status === 'Normal') {
    return 'success-row'
  } else {
    return 'warning-row'
  }
}


// get Elastic Compute Resource list
const getEIPList = () => {
  sendGetReq({
    params: {
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    },
    uri: "/eip/list"
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        eipResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get eip list error');
  });
}
getEIPList(); // init ECR list

// search ECR by project_name
const searchEip = () => {
  sendGetReq({
    uri: "/eip/search", params: {
      project_name: queryConditions.project_name,
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    }
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        eipResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Search eip error');
  });
}

const handlePageChange = (val: number) => {
  currentPageIndex.value = val;
  getEIPList();
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  getEIPList();
}
const exportXlsx = () => {
  eipResourceList.value.map((item: any) => {
    let arr = [];
    arr.push(item.api_request_id, item.instance_id, item.request_time,
        item.product_type, item.project_name,
        item.name, item.region_id, item.expired_time,
        item.allocation_id, item.instance_type, item.internet_charge_type, item.business_status,
        item.reservation_bandwidth, item.bandwidth,
        item.ip_address, item.reservation_internet_charge_type, item.charge_type, item.net_mode,
        item.allocation_time, item.status, item.reservation_active_time,
    );
    excelList.push(arr);
  });
  let WorkSheet = XLSX.utils.aoa_to_sheet(excelList);
  let new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, 'eip');
  XLSX.writeFile(new_workbook, `eip_summary.xlsx`);
};

const getDescription = (label: string) => {
  switch (label) {
    case "EIPStatus":
      return EIPStatus.value;
    case "ChargeType":
      return ChargeType.value;
    case "BusinessStatus":
      return BusinessStatus.value;
    case "ReservationInternetChargeType":
      return ReservationInternetChargeType.value;
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
