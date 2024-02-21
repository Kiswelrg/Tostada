<template>
  <div class="main flex flex-row grow h-full w-full">
    <FunctionList :functionList="functionList"/>
    <Server />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import FunctionList from './FunctionList/FunctionList.vue';
import Server from './FunctionDetail/Server/Server.vue';

const functionList = ref({
  directMessages: [
    { imageSrc: '/static/main/sffgurus.webp' },
    // Add more objects with image sources for direct messages
  ],
  joinedServers: [
    { imageSrc: '/static/main/myserver.webp' },
    { imageSrc: '/static/main/sffgurus.webp' },
    { imageSrc: '/static/main/mj.webp' },
    { imageSrc: '/static/main/mj.webp' },
    { imageSrc: '/static/main/mj.webp' },
    { imageSrc: '/static/main/mj.webp' },
    { imageSrc: '/static/main/mj.webp' },
    { imageSrc: '/static/main/mj.webp' },
    // Add more objects with image sources for joined servers
  ],
  placeholderCount: [
    { imageSrc: '/static/favicon.svg' }
  ]
});
</script>


<style scoped lang="scss">
.main {
  height: 100%;
  overflow: hidden;

  .serverlist {
    background-color: #1e1f22;
    width: 72px;
    margin: 0;
    -ms-overflow-style: none;  /* Internet Explorer 10+ */
    scrollbar-width: none;

    &>* {
      padding: 0;
      margin: 0;
    }

    >:first-child {
      margin-top: 12px;
    }

  }

  .serverlist::-webkit-scrollbar {
    display: none;
  }
}


</style>
