<!--Application Server load balancer-->
<template>
  <div>
    <div class="product_container">
      <div class="handle-box">

        <el-input v-model="queryConditions.project_name" @keydown.enter="searchAlb" :placeholder=t(base_i18n.project_name) class="handle-input mr10"></el-input>
        <el-button color="#626aef" :icon="Search" type="primary" @click="searchAlb">{{ t(base_i18n.search) }}</el-button>
        <el-button :icon="Refresh" type="primary" @click="getALBList" style="float: right">{{ t(base_i18n.refresh) }}</el-button>
        <el-button type="primary" @click="exportXlsx" style="float: right">{{ t(base_i18n.export) }}</el-button>
      </div>

      <el-scrollbar>
        <el-table :data="albResourceList"
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
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.instance_id) }}: {{ props.row.instance_id }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.product_type) }}: {{ props.row.product_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.address_ip_version) }}: {{ props.row.address_ip_version }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.address_allocated_mode) }}: {{ props.row.address_allocated_mode }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.address_type) }}: {{ props.row.address_type }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.dns_name) }}: {{ props.row.dns_name }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.load_balancer_bussiness_status) }}: {{ props.row.load_balancer_bussiness_status }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(lb_i18n.load_balancer_edition) }}: {{ props.row.load_balancer_edition }}</p>
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
          <el-table-column :render-header="renderHeader" prop="load_balancer_status" align="center" :label=t(lb_i18n.load_balancer_status) show-overflow-tooltip width="165px"></el-table-column>
          <el-table-column :render-header="renderHeader" prop="load_balancer_edition" align="center" :label=t(lb_i18n.load_balancer_edition) show-overflow-tooltip width="180px"></el-table-column>

          <el-table-column align="center" prop="load_balancer_bussiness_status" :label=t(lb_i18n.load_balancer_bussiness_status) show-overflow-tooltip width="250px" font-weight: bold></el-table-column>
          <el-table-column align="center"  :label=t(base_i18n.create_time) show-overflow-tooltip width="250px" font-weight: bold>
            <template #default="scope">
              <div style="font-weight: bold">
                {{ changeTimePattern(scope.row.create_time) }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="load_balancer_name" align="center" :label=t(lb_i18n.load_balancer_name) show-overflow-tooltip width="180px"></el-table-column>
          <el-table-column prop="pay_type" align="center" :label=t(base_i18n.project_name) show-overflow-tooltip width="150px"></el-table-column>
          <el-table-column :render-header="renderHeader" prop="address_type" :label=t(lb_i18n.address_type) align="center" width="180px"></el-table-column>
          <el-table-column :render-header="renderHeader" align="center" :label=t(lb_i18n.address_allocated_mode) show-overflow-tooltip width="200px" color:red>
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.address_allocated_mode }}
              </div>
            </template>
          </el-table-column>


          <el-table-column prop="dns_name" :label=t(lb_i18n.dns_name) align="center" width="100px" show-overflow-tooltip>
          </el-table-column>


          <el-table-column :render-header="renderHeader" prop="address_ip_version" align="center" :label=t(lb_i18n.address_ip_version) show-overflow-tooltip width="160px"></el-table-column>
          <el-table-column prop="ipv6_address_type" align="center" :label=t(lb_i18n.ipv6_address_type) show-overflow-tooltip width="180px"></el-table-column>


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
import {changeTimePattern, lb_i18n, base_i18n} from "~/stores/utils";

const {t} = useI18n()
const parentBorder = ref(true)
const auth = ['admin', 'user']
const small = ref(false)
const background = ref(true)
const disabled = ref(false)


const LoadBalancerStatus = ref("" +
    "(Inactive, 已停止)--" +
    " (Active, 运行中)--" +
    " (Provisioning, 创建中)--" +
    " (Configuring, 变配中)--" +
    " (CreateFailed, 创建失败)")

const LoadBalancerEdition = ref("" +
    "(Basic, 基础版)" +
    " (Standard, 标准版)" +
    " (StandardWithWaf, WAF增强版)")

const AddressAllocatedMode = ref("" +
    "(Fixed, 固定IP模式)" +
    " (Dynamic, 动态IP模式)")

const AddressIpVersion = ref("" +
    "(Ipv4, IPv4类型)--" +
    " (DualStack, 双栈类型)")

const AddressType = ref("" +
    "(internet, 公网负载均衡)" +
    " (intranet, 内网负载均衡)")


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
interface albResource {
  api_request_id: any,
  instance_id: string,
  request_time: string,
  product_type: string,
  project_name: string,
  create_time: string,
  address_allocated_mode: string,
  address_type: string,
  dns_name: string,
  pay_type: string,
  load_balancer_bussiness_status: string,
  load_balancer_edition: string,
  load_balancer_name: string,
  load_balancer_status: string,
  address_ip_version: string,
  ipv6_address_type: string,
}

const excelList = [[
  'api_request_id',
  'instance_id',
  'request_time',
  'product_type',
  'project_name',
  'create_time',
  'address_allocated_mode',
  'address_type',
  'dns_name',
  'pay_type',
  'load_balancer_bussiness_status',
  'load_balancer_edition',
  'load_balancer_name',
  'load_balancer_status',
  'address_ip_version',
  'ipv6_address_type',
]];
const albResourceList = ref<albResource[]>([]);
const pageTotal = ref(0);

// The conditions of search api
const queryConditions = reactive({
  project_name: "",
});

let currentPageIndex = ref(1);
let pageSize = ref(10);

const tableRowClassName = ({row}: { row: albResource }) => {
  if (row.load_balancer_status === 'Active') {
    return 'success-row'
  } else {
    return 'warning-row'
  }
}


// get Elastic Compute Resource list
const getALBList = () => {
  sendGetReq({
    params: {
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    },
    uri: "/alb/list"
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        albResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get alb list error');
  });
}
getALBList(); // init ECR list

// search ECR by project_name
const searchAlb = () => {
  sendGetReq({
    uri: "/alb/search", params: {
      project_name: queryConditions.project_name,
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    }
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        albResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Search alb error');
  });
}

const handlePageChange = (val: number) => {
  currentPageIndex.value = val;
  getALBList();
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  getALBList();
}

const exportXlsx = () => {
  albResourceList.value.map((item: any) => {
    let arr = [];
    arr.push(item.api_request_id, item.instance_id, item.request_time,
        item.product_type, item.project_name, item.create_time, item.address_allocated_mode,
        item.address_type, item.dns_name, item.pay_type, item.load_balancer_bussiness_status,
        item.load_balancer_edition, item.load_balancer_name, item.load_balancer_status, item.address_ip_version,
        item.ipv6_address_type
    );
    excelList.push(arr);
  });
  let WorkSheet = XLSX.utils.aoa_to_sheet(excelList);
  let new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, 'alb');
  XLSX.writeFile(new_workbook, `alb_summary.xlsx`);
};

const getDescription = (label: string) => {
  switch (label) {
    case "LoadBalancerStatus":
      return LoadBalancerStatus.value;
    case "LoadBalancerEdition":
      return LoadBalancerEdition.value;
    case "AddressAllocatedMode":
      return AddressAllocatedMode.value;
    case "AddressIpVersion":
      return AddressIpVersion.value;
    case "AddressType":
      return AddressType.value;
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
