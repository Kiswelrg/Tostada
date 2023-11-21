<script setup>

</script>

<template>
  <div class="main flex flex-row grow h-full w-full">
    <div class="serverlist flex flex-col overflow-y-scroll">
      <!-- Direct Message icons -->
      <div class="sublist flex-1 mx-0 grow-0">
        <div class="flex flex-col w-full">
          <div class="h-12 relative flex mx-auto mb-2" v-for="(message, index) in directMessages" :key="index">
            <div>
              
            </div>
            <!-- Your direct message icons here -->
            <span class="icon inline-block w-12">
              <img :src="message.imageSrc" alt="Direct Message" class="icon mx-auto rounded-full hover:rounded-2xl transition duration-300 ease-in-out" />
            </span>
          </div>
        </div>
      </div>

      <div>
        <div class="delimeter h-0.5 w-8 flex-1 mx-auto mb-2">

        </div>
      </div>
      <!-- User's joined servers icons -->
      <div class="sublist flex-1 mx-0 grow-0">
        <div class="flex flex-col w-full">
          <div class="h-12 relative flex mx-auto mb-2"  v-for="(server, index) in joinedServers" :key="index">
            <div class="absolute w-0.5 h-2 white block left-0 inset-y-auto">

            </div>
            <!-- Your joined servers icons here -->
            <span class="icon inline-block w-12">
              <img :src="server.imageSrc" alt="Direct Message" class="icon relative mx-auto rounded-full hover:rounded-2xl transition duration-300 ease-in-out" />
            </span>
          </div>
        </div>
      </div>

      <div>
        <div class="delimeter h-0.5 w-8 flex-1 mx-auto mb-2">

        </div>
      </div>

      <!-- Placeholder icons -->
      <div class="sublist flex-1 mx-0 grow-0">
        <div class="flex flex-col w-full">
          <div class="h-12 relative flex mx-auto mb-2"  v-for="(func, index) in placeholderCount" :key="index">
            <!-- Your placeholder icons here -->
            <span class="icon inline-block w-12">
              <img :src="func.imageSrc" alt="Direct Message" class="icon relative mx-auto rounded-full hover:rounded-2xl transition duration-300 ease-in-out" />
            </span>
          </div>
        </div>
      </div>
    </div>
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

    .delimeter {
      background-color: #35363c;
      border-radius: 1px;
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
