<!--Application Server load balancer-->
<template>
  <div>
    <div class="product_container">
      <div class="handle-box">

        <el-input v-model="queryConditions.project_name" @keydown.enter="searchSlb" :placeholder=t(base_i18n.project_name) class="handle-input mr10"></el-input>
        <el-button color="#626aef" :icon="Search" type="primary" @click="searchSlb">{{ t(base_i18n.search) }}</el-button>
        <el-button :icon="Refresh" type="primary" @click="getSLBList" style="float: right">{{ t(base_i18n.refresh) }}</el-button>
        <el-button type="primary" @click="exportXlsx" style="float: right">{{ t(base_i18n.export) }}</el-button>
      </div>

      <el-scrollbar>
        <el-table :data="slbResourceList"
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
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.pay_type) }}: {{ props.row.pay_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.internet_charge_type) }}: {{ props.row.internet_charge_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.load_balancer_name) }}: {{ props.row.load_balancer_name }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.address) }}: {{ props.row.address }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.address_type) }}: {{ props.row.address_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.address_ip_version) }}: {{ props.row.address_ip_version }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.region_id) }}: {{ props.row.region_id }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.load_balancer_status) }}: {{ props.row.load_balancer_status }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.load_balancer_spec) }}: {{ props.row.load_balancer_spec }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.instance_charge_type) }}: {{ props.row.instance_charge_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.master_zone_id) }}: {{ props.row.master_zone_id }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.slave_zone_id) }}: {{ props.row.slave_zone_id }}</p>
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
          <el-table-column align="center" :label=t(base_i18n.create_time) show-overflow-tooltip width="250px" font-weight: bold>
            <template #default="scope">
              <div style="font-weight: bold">
                {{ changeTimePattern(scope.row.create_time) }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="pay_type" align="center" :label=t(base_i18n.project_name) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="bandwidth" align="center" :label=t(base_i18n.bandwidth) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="end_time_stamp" align="center" :label=t(base_i18n.end_time_stamp) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="end_time" align="center" :label=t(base_i18n.end_time) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="auto_release_time" align="center" :label=t(base_i18n.auto_release_time) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="renewal_status" align="center" :label=t(base_i18n.renewal_status) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="renewal_duration" align="center" :label=t(base_i18n.renewal_duration) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column prop="renewal_cyc_unit" align="center" :label=t(base_i18n.renewal_cyc_unit) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column :render-header="renderHeader" prop="load_balancer_status" align="center" :label=t(lb_i18n.load_balancer_status) show-overflow-tooltip width="165px"></el-table-column>
          <el-table-column :render-header="renderHeader" prop="internet_charge_type" align="center" :label=t(base_i18n.internet_charge_type) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column prop="load_balancer_name" align="center" :label=t(lb_i18n.load_balancer_name) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column align="center" prop="address" :label=t(base_i18n.address) show-overflow-tooltip width="250px" font-weight: bold></el-table-column>
          <el-table-column :render-header="renderHeader" prop="address_type" :label=t(lb_i18n.address_type) align="center" width="180px"></el-table-column>
          <el-table-column :render-header="renderHeader" align="center" :label=t(lb_i18n.address_ip_version) show-overflow-tooltip width="200px" color:red>
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.address_ip_version }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="region_id" :label=t(base_i18n.region_id) align="center" width="100px" show-overflow-tooltip></el-table-column>
          <el-table-column :render-header="renderHeader" prop="load_balancer_spec" align="center" :label=t(lb_i18n.load_balancer_spec) show-overflow-tooltip width="160px"></el-table-column>
          <el-table-column prop="instance_charge_type" align="center" :label=t(base_i18n.instance_charge_type) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column prop="master_zone_id" align="center" :label=t(base_i18n.master_zone_id) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column prop="slave_zone_id" align="center" :label=t(base_i18n.slave_zone_id) show-overflow-tooltip width="180px"></el-table-column>
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
import {changeTimePattern, lb_i18n, base_i18n, ecs_i18n} from "~/stores/utils";

const {t} = useI18n()
const parentBorder = ref(true)
const auth = ['admin', 'user']
const small = ref(false)
const background = ref(true)
const disabled = ref(false)


const RenewalStatus = ref("" +
    "(AutoRenewal, 自动续费)--" +
    " (Normal, 非自动续费)--" +
    " (NotRenewal, 不再续费)--")




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
interface slbResource {
  api_request_id: any,
  instance_id: string,
  request_time: string,
  product_type: string,
  project_name: string,

  bandwidth: number,
  end_time_stamp: number,
  end_time: string,
  auto_release_time: number,
  renewal_status: string,
  renewal_duration: number,
  renewal_cyc_unit: string,

  create_time: string,
  pay_type: string,
  internet_charge_type: string,
  load_balancer_name: string,
  address: string,
  address_type: string,
  address_ip_version: string,
  region_id: string,
  load_balancer_status: string,
  load_balancer_spec: string,
  instance_charge_type: string,
  master_zone_id: string,
  slave_zone_id: string,
}

const excelList = [[
  'api_request_id',
  'instance_id',
  'request_time',
  'product_type',
  'project_name',
  'bandwidth',
  'end_time_stamp',
  'end_time',
  'auto_release_time',
  'renewal_status',
  'renewal_duration',
  'renewal_cyc_unit',
  'create_time',
  'pay_type',
  'internet_charge_type',
  'load_balancer_name',
  'address',
  'address_type',
  'address_ip_version',
  'region_id',
  'load_balancer_status',
  'load_balancer_spec',
  'instance_charge_type',
  'master_zone_id',
  'slave_zone_id',
]];
const slbResourceList = ref<slbResource[]>([]);
const pageTotal = ref(0);

// The conditions of search api
const queryConditions = reactive({
  project_name: "",
});

let currentPageIndex = ref(1);
let pageSize = ref(10);

const tableRowClassName = ({row}: { row: slbResource }) => {
  if (row.load_balancer_status === 'Active') {
    return 'success-row'
  } else {
    return 'warning-row'
  }
}


// get Elastic Compute Resource list
const getSLBList = () => {
  sendGetReq({
    params: {
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    },
    uri: "/slb/list"
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        slbResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get alb list error');
  });
}
getSLBList(); // init ECR list

// search ECR by project_name
const searchSlb = () => {
  sendGetReq({
    uri: "/slb/search", params: {
      project_name: queryConditions.project_name,
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    }
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        slbResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Search alb error');
  });
}

const handlePageChange = (val: number) => {
  currentPageIndex.value = val;
  getSLBList();
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  getSLBList();
}
const exportXlsx = () => {
  slbResourceList.value.map((item: any) => {
    let arr = [];
    arr.push(item.api_request_id, item.instance_id, item.request_time,
        item.product_type, item.project_name,
        item.bandwidth, item.end_time_stamp, item.end_time,
        item.auto_release_time, item.renewal_status, item.renewal_duration, item.renewal_cyc_unit,
        item.create_time, item.pay_type,
        item.internet_charge_type, item.load_balancer_name, item.address, item.address_type,
        item.address_ip_version, item.region_id, item.load_balancer_status, item.load_balancer_spec,
        item.instance_charge_type, item.master_zone_id, item.slave_zone_id,
    );
    excelList.push(arr);
  });
  let WorkSheet = XLSX.utils.aoa_to_sheet(excelList);
  let new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, 'slb');
  XLSX.writeFile(new_workbook, `slb_summary.xlsx`);
};

const getDescription = (label: string) => {
  switch (label) {
    case "RenewalStatus":
      return RenewalStatus.value;
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
