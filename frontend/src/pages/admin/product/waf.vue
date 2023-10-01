<!--Elastic Compute Service-->
<template>

  <div>
    <div class="product_container">
      <div class="handle-box">
        <el-select v-model="queryConditions.cloud_platform" :placeholder=t(waf_i18n.region) class="handle-select mr10">
          <el-option
              v-for="item in regionOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
        <el-input v-model="queryConditions.project_name" @keydown.enter="searchWaf" :placeholder=t(base_i18n.projectName) class="handle-input mr10"></el-input>
        <el-button color="#626aef" :icon="Search" type="primary" @click="searchWaf">{{ t(base_i18n.search) }}</el-button>
        <el-button :icon="Refresh" type="primary" @click="getWAFList" style="float: right">{{ t(base_i18n.refresh) }}</el-button>
        <el-button type="primary" @click="exportXlsx" style="float: right">{{ t(base_i18n.export) }}</el-button>
      </div>

      <el-scrollbar>
        <el-table :data="WAFResourceList"
                  border
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
                <p m="t-0 b-2" style="font-weight: bold">{{ t(waf_i18n.waf_start_time) }}: {{ changeTimePattern(props.row.start_time) }}</p><br>
                <p m="t-0 b-2" style="font-weight: bold">{{ t(base_i18n.instance_id) }}: {{ props.row.instance_id }}</p><br>
              </div>
            </template>
          </el-table-column>

          <el-table-column align="center" :label=t(waf_i18n.region) show-overflow-tooltip width="150px" font-weight: bold :render-header="renderHeader">
            <template #default="scope" style="font-weight: bold">
              <div style="font-weight: bold">
                {{ scope.row.region == 'ap-southeast-1' ? 'Oversea' : 'Mainland' }}
              </div>
            </template>
          </el-table-column>

          <el-table-column :label=t(waf_i18n.waf_status) align="center" width="130px" :render-header="renderHeader">
            <template #default="scope">
              <el-tag :type="scope.row.waf_status === 1 ? 'success' : 'danger'">
                {{ scope.row.waf_status === 1 ? 'Running' : 'Expired/Released' }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column align="center" :label=t(waf_i18n.end_time) show-overflow-tooltip width="150px">
            <template #default="scope">
              <el-tag>
                {{ (timestampToTime(scope.row.end_time)) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column align="center" :label=t(base_i18n.project) show-overflow-tooltip width="130px">
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.project_name }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="product_type" align="center" :label=t(base_i18n.product_type) show-overflow-tooltip width="130px">
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.product_type.toString().toUpperCase() }}
              </div>
            </template>
          </el-table-column>
          <el-table-column align="center" :label=t(waf_i18n.edition) show-overflow-tooltip width="130px" :render-header="renderHeader">
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.edition }}
              </div>
            </template>
          </el-table-column>
          <el-table-column align="center" :label=t(waf_i18n.pay_type) show-overflow-tooltip width="130px" :render-header="renderHeader">
            <template #default="scope">
              <div style="font-weight: bold">
                {{ scope.row.pay_type }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="in_debt" align="center" :label=t(waf_i18n.in_debt) show-overflow-tooltip width="130px" :render-header="renderHeader"></el-table-column>
          <el-table-column prop="api_request_id" align="center" :label=t(base_i18n.api_request_id) show-overflow-tooltip width="130px"></el-table-column>
          <el-table-column align="center" :label=t(base_i18n.request_time) show-overflow-tooltip width="180px">
            <template #default="scope">
              <el-tag>
                {{ changeTimePattern(scope.row.request_time) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="product_type" align="center" :label=t(base_i18n.product_type) show-overflow-tooltip width="130px"></el-table-column>
          <el-table-column align="center" :label=t(waf_i18n.waf_start_time) show-overflow-tooltip width="230px">
            <template #default="scope">
              <el-tag>
                {{ changeTimePattern(scope.row.start_time) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="instance_id" align="center" :label=t(base_i18n.instance_id) show-overflow-tooltip width="200px"></el-table-column>
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
import {ref, reactive, h} from 'vue';
import {ElMessage, ElTooltip} from 'element-plus';
import {Search, Refresh} from '@element-plus/icons-vue';
import router from "@/plugins/router";
import * as XLSX from "xlsx";
import {changeTimePattern, waf_i18n, base_i18n} from "~/stores/utils";

const {t} = useI18n()

const auth = ['admin', 'user']
const small = ref(false)
const background = ref(true)
const disabled = ref(false)
const regionOptions = [
  {
    value: '非中国大陆',
    label: 'Oversea',
  },
  {
    value: '中国大陆',
    label: 'Mainland',
  },
]

const StatusDescription = ref("" +
    "(Running, 正常)--" +
    "(Expired/Released, 到期/释放)")

const EditionDescription = ref("" +
    "(Basic, 基础版)--" +
    "(Pro, 高级版)--" +
    "(Business, 企业版)--" +
    "(Enterprise, 旗舰版)")

const RegionDescription = ref("" +
    "(Mainland, 中国内地)--" +
    "(Oversea, 非中国内地)")

const PayTypeDescription = ref("" +
    "(POSTPAY, 已开通按量付费WAF实例)--" +
    "(PREPAY, 表示已开通包年包月WAF实例)")

const InDebt = ref("" +
    "(1, 表示已欠费)--" +
    "(0, 表示正常)"
)

const getDescription = (label: string) => {
  switch (label) {
    case "Status":
      return StatusDescription.value;
    case "Edition":
      return EditionDescription.value;
    case "Region":
      return RegionDescription.value;
    case "Pay Type":
      return PayTypeDescription.value;
    case "In Debt":
      return InDebt.value;
    default:
      return "-";
  }
}

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
interface WAFResource {
  api_request_id: any,
  instance_id: string,
  request_time: string,
  product_type: string,
  project: string,
  waf_status: number,
  end_time: bigint,
  edition: string,
  region: string,
  pay_type: number,
  in_debt: number,
  start_time: number,
}

const excelList = [[
  'api_request_id',
  'instance_id',
  'request_time',
  'product_type',
  'project',
  'waf_status',
  'start_time',
  'end_time',
  'edition',
  'region',
  'pay_type',
  'in_debt',
]];
const WAFResourceList = ref<WAFResource[]>([]);
const pageTotal = ref(0);

// The conditions of search api
const queryConditions = reactive({
  cloud_platform: "",
  project_name: "",
});

let currentPageIndex = ref(1);
let pageSize = ref(10);

const tableRowClassName = ({row}: { row: WAFResource }) => {
  if (row.waf_status === 1) {
    return 'success-row'
  } else {
    return 'warning-row'
  }
}


// get Elastic Compute Resource list
const getWAFList = () => {
  sendGetReq({
    params: {
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    },
    uri: "/waf/list"
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        WAFResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get ecr list error');
  });
}
getWAFList()
const initlist = () => {
  sendGetReq({
    params: {},
    uri: "/waf/init"
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        WAFResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get ecr list error');
  });
}
// initlist()

// search ECR by cloud_platform and project_name
const searchWaf = () => {
  sendGetReq({
    uri: "/waf/search", params: {
      cloud_platform: queryConditions.cloud_platform,
      project_name: queryConditions.project_name,
      page_index: currentPageIndex.value,
      page_size: pageSize.value
    }
  }).then((res) => {
        pageTotal.value = parseInt(res.data.total)
        WAFResourceList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Search project error');
  });
}
const exportXlsx = () => {
  WAFResourceList.value.map((item: any) => {
    let arr = [];
    arr.push(item.api_request_id, item.instance_id, item.request_time,
        item.product_type, item.project_name, item.waf_status, item.start_time, item.end_time,
        item.edition, item.region, item.pay_type,
        item.in_debt
    );
    excelList.push(arr);
  });
  let WorkSheet = XLSX.utils.aoa_to_sheet(excelList);
  let new_workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(new_workbook, WorkSheet, 'waf');
  XLSX.writeFile(new_workbook, `waf_summary.xlsx`);
};

function timestampToTime(timestamp) {
  // 时间戳为10位需*1000，时间戳为13位不需乘1000
  let date = new Date(timestamp);
  let Y = date.getFullYear() + "-";
  let M =
      (date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1) + "-";
  let D = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + " ";
  return Y + M + D;
}

const handlePageChange = (val: number) => {
  currentPageIndex.value = val;
  getWAFList();
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  getWAFList();
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
  --el-table-tr-bg-color: let(--el-color-warning-light-9);
}

.el-table .success-row {
  --el-table-tr-bg-color: let(--el-color-success-light-9);
}

</style>
