<template>
	<div :style="{backgroundImage:'url('+bgImg+')'}"></div>
	<div>
		<div class="grid grid-cols-3">
			<a href="https://www.sunthycloud.com" target="_blank">
				<img src="/logo.svg" class="logo" alt="logo"/>
			</a>
		</div>
		<HelloWorld msg="Sunthy Cloud Monitor"/>
	</div>
</template>
<script>
import bgImg from "../../public/logo.svg"
export default {
    name: 'App',
    data () {
        return {
            bgImg: bgImg,
        }
    }
}
</script>
<style>
a {
	color: rgba(37, 99, 235);
}

p {
	padding: 0 10px;
}

.logo {
	position: absolute;
	left: 39%;
	width: 30em;
	height: 30em;
	padding: 1.5rem;
	will-change: filter;
	transition: filter 300ms;
}

.logo:hover {
	filter: drop-shadow(0 0 2em #646cffaa);
}

</style>
