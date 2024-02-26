<template>
  <div class="main flex flex-row grow h-full w-full">
    <FunctionList :functionList="functionList" @update-active-server-tab="onUpdateActiveServerTab" @go-tab="onGoTab"></FunctionList>
    <MeVue v-if="isMeActive"></MeVue>
    <ServerVue v-else :server="activeServer"></ServerVue>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { provide } from 'vue';
import session from "@/util/session";

import FunctionList from './FunctionList/FunctionList.vue';
import ServerVue from '@/i/FunctionDetail/Server/Server.vue'
import MeVue from '@/i/FunctionDetail/me/me.vue'

const activeServerTab = ref(-1);
const isMeActive = ref(true);
const route = useRoute();
const router = useRouter();

const functionList = ref({
  directMessages: [
    { logoSrc: '/static/tool/main/user-solid.svg' },
    // Add more objects with image sources for direct messages
  ],
  joinedServers: [
    // Add more objects with image sources for joined servers
  ],
  placeholderCount: [
    { logoSrc: '/static/favicon.svg' }
  ]
});

onMounted(() => {
  (async () => {
    await fetchToolServers();
    if ( route.name == 'tool-root') {
      if ( functionList.value['joinedServers'].length == 0 ) {
        console.log('open find-server panel');
      } else {
        activeServerTab.value = 0;
        
      }
    
  }
  })();
  isMeActive.value = route.meta.isMeActive;
  
});


const activeServer = computed(() => {
  if (activeServerTab.value == -1) return undefined
  return functionList.value['joinedServers'][activeServerTab.value]
})
provide('active-server', activeServer)

function setFunctionList(ss) {
  functionList.value['joinedServers'] = ss['tool_servers'];
}

function onUpdateActiveServerTab(tabIndex) {
  activeServerTab.value = tabIndex;
}

function onGoTab(path) {
  if (path == router.resolve({name: 'tool-me'}).path) {
    if (isMeActive.value) return;
    
    isMeActive.value = true;

  } else if (path == router.resolve({name: 'tool-root'}).path) {
    if (!isMeActive.value) return;

    isMeActive.value = false;
  } else {
    console.log('error:', path);
  }
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
    setFunctionList(r);
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
