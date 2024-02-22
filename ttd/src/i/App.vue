<template>
  <div class="main flex flex-row grow h-full w-full">
    <ServerList :serverList="serverList" />
    <Server />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import session from "@/util/session";

import ServerList from './FunctionList/FunctionList.vue';
import Server from './FunctionDetail/Server/Server.vue';
onMounted(() => {
  (async () => {
    await fetchToolServers();
  })();
});

const serverList = ref({
  directMessages: [
    { logoSrc: '/static/tool/main/user-solid.svg' },
    // Add more objects with image sources for direct messages
  ],
  joinedServers: [
    { logoSrc: '/static/tool/server_list/myserver.webp' },
    { logoSrc: '/static/tool/server_list/sffgurus.webp' },
    { logoSrc: '/static/tool/server_list/mj.webp' },
    { logoSrc: '/static/tool/server_list/mj.webp' },
    { logoSrc: '/static/tool/server_list/mj.webp' },
    { logoSrc: '/static/tool/server_list/mj.webp' },
    { logoSrc: '/static/tool/server_list/mj.webp' },
    { logoSrc: '/static/tool/server_list/mj.webp' },
    // Add more objects with image sources for joined servers
  ],
  placeholderCount: [
    { logoSrc: '/static/favicon.svg' }
  ]
});

function setServerList(ss) {
  serverList.value['joinedServers'] = ss['tool_servers'];
}

async function fetchToolServers() {
  const response = await fetch(
    "/api/i/user/tool_servers/",
    {
      method: "GET",
    }
  );

  if (response.ok) {
    const r = await response.json();
    console.log(r);
    setServerList(r);
  } else {
    console.log(response.status);
  }
}
</script>


<style scoped lang="scss">
.main {
  height: 100%;
  overflow: hidden;

  .serverlist {
    background-color: #1e1f22;
    width: 72px;
    margin: 0;
    -ms-overflow-style: none;
    /* Internet Explorer 10+ */
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
