<template>
  <BlogHeader />

  <ArticleList />
  <div>
    <div class="grid grid-cols-3">
      <a href="https://vitejs.dev" target="_blank">
        <img src="/logo.svg" class="logo" alt="Vite logo"/>
      </a>
    </div>
  </div>

  <BlogFooter />
</template>

<script setup>
import BlogHeader from "@/components/BlogHeader.vue"
import BlogFooter from "@/components/BlogFooter.vue"
import ArticleList from "@/components/ArticleList.vue"
</script>


<style>
a {
  color: rgba(37, 99, 235);
}

p {
  padding: 0 10px;
}

.logo {
  width: 10em;
  height: 10em;
  padding: 1.5rem;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
