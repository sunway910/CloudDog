<template>
	<el-footer class="app-foot">{{ footerMsgCopyright }}</el-footer>
</template>

<script lang="ts">
export default {
	name: 'AppFoot',
	data() {
		return {
			footerMsgCopyright: 'Copyright © 2022-2023 SunthyCloud',
		}
	}
}
</script>

<style>
.app-foot {
	min-height: 20px;
	width: 100%;
	font-size: 10px;
	display: flex;
	align-items: center;
	justify-content: center;
	position: absolute;
	right: 0;
	bottom: 0;
	left: 0;
}
</style>
