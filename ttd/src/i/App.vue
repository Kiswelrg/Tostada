<script setup>
import FunctionList from './FunctionList/FunctionList.vue';
import Server from './FunctionDetail/Server/Server.vue';
</script>

<template>
  <div class="main flex flex-row grow h-full w-full">
    <FunctionList :functionList="functionList"/>
    <Server />
  </div>
</template>

<script>
export default {
  data() {
    return {
      functionList: {
        directMessages: [
          { imageSrc: '../../src/assets/main/sffgurus.webp' },
          // Add more objects with image sources for direct messages
        ],
        joinedServers: [
          { imageSrc: '../../src/assets/main/myserver.webp' },
          { imageSrc: '../../src/assets/main/sffgurus.webp' },
          { imageSrc: '../../src/assets/main/mj.webp' },
          { imageSrc: '../../src/assets/main/mj.webp' },
          { imageSrc: '../../src/assets/main/mj.webp' },
          { imageSrc: '../../src/assets/main/mj.webp' },
          { imageSrc: '../../src/assets/main/mj.webp' },
          { imageSrc: '../../src/assets/main/mj.webp' },
          // Add more objects with image sources for joined servers
        ],
        placeholderCount: [
          { imageSrc: '/tostada.svg' }
        ]
      }
    };
  }
  // You can fetch data or set your icons' image sources within the directMessages and joinedServers arrays.
};
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
