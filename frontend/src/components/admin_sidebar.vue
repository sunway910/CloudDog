<template>
  <div class="admin_sidebar">
    <el-menu
        class="sidebar-el-menu"
        :default-active="onRoutes"
        :collapse="sidebar.collapse"
        background-color="#324157"
        text-color="#bfcbd9"
        active-text-color="#20a0ff"
        unique-opened
        router
    >
      <template v-for="item in items">
        <template v-if="item.subs">
          <el-sub-menu :index="item.index" :key="item.index" v-auth="item.auth">
            <template #title>
              <el-icon>
                <component :is="item.icon"></component>
              </el-icon>
              <span>{{ t(item.title) }}</span>
            </template>
            <template v-for="subItem in item.subs">
              <el-menu-item :index="subItem.index" v-auth="item.auth">
                {{ t(subItem.title) }}
              </el-menu-item>
            </template>
          </el-sub-menu>
        </template>
        <template v-else>
          <el-menu-item :index="item.index" :key="item.index" v-auth="item.auth">
            <el-icon>
              <component :is="item.icon"></component>
            </el-icon>
            <template #title>{{ t(item.title) }}</template>
          </el-menu-item>
        </template>
      </template>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import {computed} from 'vue';
import {useSidebarStore} from '@/stores/sidebar';
import {useRoute} from 'vue-router';

const {t, locale} = useI18n()

const toggleLocale = () => {
  // locale.value 用来表示当前所属语言，可修改进行语言切换
  locale.value = locale.value === 'zh-CN' ? 'en' : 'zh-CN'
}
const items = [
  {
    // icon : https://element-plus.org/en-US/component/icon.html
    icon: 'Odometer',
    index: '/admin/overview',
    title: 'Overview',
    auth: 'user',
    subs: null,
  },
  {
    icon: 'Monitor',
    index: '2',
    title: 'Monitor',
    auth: 'user',
    subs: [
      {
        index: '/admin/product/ecs',
        title: 'ECR',
        auth: 'user',
      },
      {
        index: '/admin/product/waf',
        title: 'WAF',
        auth: 'user',
      },
    ],
  },
  {
    icon: 'DocumentCopy',
    title: 'Manager',
    index: '3',
    auth: 'user',
    subs: [
      {
        index: '/admin/system/job',
        title: 'Job',
        auth: 'admin',
      },
      {
        index: '/admin/system/job_history',
        title: 'History',
        auth: 'admin',
      },
      {
        index: '/admin/system/messages',
        title: 'Message',
        auth: 'user',
      },
    ],
  },
  {
    icon: 'Warning',
    title: 'Auth',
    index: '4',
    auth: 'admin',
    subs: [
      {
        index: '/admin/auth/user',
        title: 'User',
        auth: 'admin',
      },
    ],
  },
];

const route = useRoute();
const onRoutes = computed(() => {
  return route.path;
});

const sidebar = useSidebarStore();
</script>

<style scoped>
.admin_sidebar {
  display: block;
  position: absolute;
  left: 0;
  top: 70px;
  bottom: 0;
  overflow-y: scroll;
}

.admin_sidebar::-webkit-scrollbar {
  width: 0;
}

.sidebar-el-menu:not(.el-menu--collapse) {
  width: 250px;
}

.admin_sidebar > ul {
  height: 100%;
}
</style>
