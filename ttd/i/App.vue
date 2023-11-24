<script setup>
import FunctionList from './FunctionList/FunctionList.vue';
</script>

<template>
  <div class="main flex flex-row grow h-full w-full">
    <FunctionList :functionList="functionList"/>
    <div class="server flex flex-row w-full">
      <div class="toollist flex flex-auto bg-orange-100"></div>
      <div class="tooldetail flex grow basis-full bg-orange-50 w-full"></div>
    </div>
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
          // Add more objects with image sources for joined servers
        ],
        placeholderCount: [
          { imageSrc: '../../src/assets/main/myserver.webp' },
          { imageSrc: '../../src/assets/main/sffgurus.webp' },
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

  .server {
    .toollist {
      background-color: #2b2d31;
      width: 240px;
    }

    .tooldetail {
      background-color: #313338;
    }
  }
}


</style>
