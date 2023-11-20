<script setup>
import HelloWorld from './components/HelloWorld.vue'
import DevHeader from '../src/components/DevHeader.vue';
</script>

<template>
  <div class="bg-teal-100">
    <a href="https://vitejs.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
    <DevHeader></DevHeader>
  </div>
  <div class="main flex flex-row grow h-full w-full">
    <div class="serverlist flex bg-gray-950"></div>
    <div class="server flex flex-row w-full">
      <div class="toollist flex flex-auto bg-gray-800"></div>
      <div class="tooldetail flex grow basis-full bg-gray-400 w-full"></div>
    </div>
  </div>
  <HelloWorld msg="Vite + Vue" />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
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
