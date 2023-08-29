<template>
	<div class="auth_container">

		<div class="auth_plugins-tips">
			Use custom command `v-auth` to control permission
		</div>

		<div class="auth_mgb20">
			<span class="label">Role: </span>
			<el-select v-model="role" @change="handleChange">
				<el-option label="admin" value="admin"></el-option>
				<el-option label="user" value="user"></el-option>
			</el-select>
		</div>
		<div class="auth_mgb20 tree-wrapper">
			<el-tree
				ref="tree"
				:data="data"
				node-key="id"
				default-expand-all
				show-checkbox
				:default-checked-keys="checkedKeys"
			/>
		</div>
		<el-button type="primary" @click="onSubmit">Save</el-button>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ElTree } from 'element-plus';
import { useAuthStore } from '@/stores/auth';

const role = ref<string>('admin');

interface Tree {
	id: string;
	label: string;
	children?: Tree[];
}

const data: Tree[] = [
	{
		id: '1',
		label: '系统首页'
	},
	{
		id: '2',
		label: '基础表格',
		children: [
			{
				id: '15',
				label: '编辑'
			},
			{
				id: '16',
				label: '删除'
			}
		]
	},
	{
		id: '3',
		label: 'tab选项卡'
	},
	{
		id: '4',
		label: '表单相关',
		children: [
			{
				id: '5',
				label: '基本表单'
			},
			{
				id: '6',
				label: '文件上传'
			},
			{
				id: '7',
				label: '三级菜单',
				children: [
					{
						id: '8',
						label: '富文本编辑器'
					},
					{
						id: '9',
						label: 'markdown编辑器'
					}
				]
			}
		]
	},
	{
		id: '10',
		label: '自定义图标'
	},
	{
		id: '11',
		label: 'schart图表'
	},

	{
		id: '13',
		label: '权限管理'
	},
	{
		id: '14',
		label: '支持作者'
	}
];

const permiss = useAuthStore();

// 获取当前权限
const checkedKeys = ref<string[]>([]);
const getPremission = () => {
	// 请求接口返回权限
	checkedKeys.value = permiss.defaultList[role.value];
};
getPremission();

// 保存权限
const tree = ref<InstanceType<typeof ElTree>>();
const onSubmit = () => {
	// 获取选中的权限
	console.log(tree.value!.getCheckedKeys(false));
};

const handleChange = (val: string[]) => {
	tree.value!.setCheckedKeys(permiss.defaultList[role.value]);
};
</script>

<style scoped>
.tree-wrapper {
	max-width: 500px;
}
.label {
	font-size: 14px;
}
.auth_container {
    padding: 30px;
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 5px;
}
.auth_plugins-tips {
    padding: 20px 10px;
    margin-bottom: 20px;
}
.auth_mgb20 {
	margin-bottom: 20px;
}
.auth_plugins-tips{
    background: #eef1f6;
}
</style>
