<template>
  <div class="container">
    <el-tabs v-model="message">
      <el-tab-pane :label="`Unread(${state.unread.length})`" name="first">
        <el-table :data="state.unread" :show-header="false" style="width: 100%">
          <el-table-column>
            <template #default="scope">
              <span class="message-title">{{ scope.row.title }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="date" width="180"></el-table-column>
          <el-table-column width="120">
            <template #default="scope">
              <el-button size="small" @click="handleRead(scope.$index)">Mark as read</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="handle-row">
          <el-button type="primary">Mark as read</el-button>
        </div>
      </el-tab-pane>
      <el-tab-pane :label="`Read(${state.read.length})`" name="second">
        <template v-if="message === 'second'">
          <el-table :data="state.read" :show-header="false" style="width: 100%">
            <el-table-column>
              <template #default="scope">
                <span class="message-title">{{ scope.row.title }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="date" width="150"></el-table-column>
            <el-table-column width="120">
              <template #default="scope">
                <el-button type="danger" @click="handleDel(scope.$index)">Delete</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="handle-row">
            <el-button type="danger">Delete all</el-button>
          </div>
        </template>
      </el-tab-pane>
      <el-tab-pane :label="`Trash(${state.recycle.length})`" name="third">
        <template v-if="message === 'third'">
          <el-table :data="state.recycle" :show-header="false" style="width: 100%">
            <el-table-column>
              <template #default="scope">
                <span class="message-title">{{ scope.row.title }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="date" width="150"></el-table-column>
            <el-table-column width="120">
              <template #default="scope">
                <el-button @click="handleRestore(scope.$index)">Set back</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="handle-row">
            <el-button type="danger">Delete forever</el-button>
          </div>
        </template>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive} from 'vue';
import {ElMessage} from "element-plus";

const message = ref('first');
const state = reactive({
  unread: [
    {
      date: '2018-04-19 20:00:00',
      title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
    },
    {
      date: '2018-04-19 21:00:00',
      title: '今晚12点整发大红包，先到先得'
    }
  ],
  read: [
    {
      date: '2018-04-19 20:00:00',
      title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
    }
  ],
  recycle: [
    {
      date: '2018-04-19 20:00:00',
      title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
    }
  ]
});

interface MessageItem {
  id: number;
  project_name: string;
  instance_id: string;
  create_time: string;
  event_message: any;
  event_type: string,
  product_type: any,
  status: string,
}

let currentPageIndex = ref(1);
let pageSize = ref(10);
const unreadMessageList = ref<MessageItem[]>([]);
const readMessageList = ref<MessageItem[]>([]);
const trashMessageList = ref<MessageItem[]>([]);
const messageList = ref<MessageItem[]>([]);
const pageTotal = ref(0);
const queryConditions = reactive({
  status: "unread",
  project_name: "",
});
const getMessageList = () => {
  sendGetReq({
    uri: "/message/list",
    params: {status: "unread", page_index: currentPageIndex.value, page_size: pageSize.value}
  }).then((res) => {
        pageTotal.value = parseInt(res.data.data.length)
        unreadMessageList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get message list error');
  });
  sendGetReq({
    uri: "/message/list",
    params: {status: "read", page_index: currentPageIndex.value, page_size: pageSize.value}
  }).then((res) => {
        pageTotal.value = parseInt(res.data.data.length)
        readMessageList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get message list error');
  });
  sendGetReq({
    uri: "/message/list",
    params: {status: "trash", page_index: currentPageIndex.value, page_size: pageSize.value}
  }).then((res) => {
        pageTotal.value = parseInt(res.data.data.length)
        trashMessageList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Get message list error');
  });
}


const searchProjects = () => {
  sendGetReq({
    uri: "/project/search",
    params: {
      status: queryConditions.status,
      project_name: queryConditions.project_name,
      page_index: currentPageIndex.value,
      page_size: pageSize.value,
    }
  }).then((res) => {
        pageTotal.value = parseInt(res.data.data.length)
        messageList.value = res.data.data
      }
  ).catch((err) => {
    ElMessage.error(err || 'Search message error');
  });
}

const handleRead = (index: number) => {
  const item = state.unread.splice(index, 1);
  state.read = item.concat(state.read);
};
const handleDel = (index: number) => {
  const item = state.read.splice(index, 1);
  state.recycle = item.concat(state.recycle);
};
const handleRestore = (index: number) => {
  const item = state.recycle.splice(index, 1);
  state.read = item.concat(state.read);
};
</script>

<style>
.message-title {
  cursor: pointer;
}

.handle-row {
  margin-top: 30px;
}
</style>
