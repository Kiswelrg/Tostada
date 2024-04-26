<template>
  <div class="main flex flex-row grow h-full w-full min-h-[250px]">
    <FunctionList :functionList="functionList" @updateServerList="fetchToolServers" @update-active-server-tab="onUpdateActiveServerTab" @go-tab="onGoTab"></FunctionList>
    <MeVue v-if="isMeActive"></MeVue>
    <ServerVue v-else :server="activeServer"></ServerVue>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { provide } from 'vue';

import FunctionList from './FunctionList/FunctionList.vue';
import ServerVue from '@/i/FunctionDetail/Server/Server.vue';
import MeVue from '@/i/FunctionDetail/me/me.vue';

const activeServerTab = ref(BigInt(-1));
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
  serverButtons: [
    {
      logoSrc: '/static/tool/main/plus-solid.svg',
      scale: 0.5
    },
    // Add more objects with image sources for direct messages
  ],
  placeholderCount: [
    { logoSrc: '/static/favicon.svg' }
  ]
});

onMounted(() => {
  (async () => {
    await fetchToolServers()
    if ( route.name == 'tool-root') {
      if ( functionList.value['joinedServers'].length == 0 ) {
        console.log('open find-server panel');
      } else {
        activeServerTab.value = functionList.value['joinedServers'][0]['cid']
        
      }
    
  }
  })();
  isMeActive.value = route.meta.isMeActive
  
});


const activeServer = computed(() => {
  if (activeServerTab.value == -1 || functionList.value['joinedServers'] === undefined) return undefined
  return functionList.value['joinedServers'].find((obj) => obj.cid === activeServerTab.value)
})
provide('active-server', activeServer)

function setFunctionList(ss) {
  functionList.value['joinedServers'] = ss['tool_servers']
}

function onUpdateActiveServerTab(cid) {
  console.log('dude', cid)
  activeServerTab.value = cid
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
    const text = await response.text()
    const r = JSON.parse(text, (key, value) => {
      if (typeof value === 'string' && key === 'cid') {
        return BigInt(value)
      }
      return value
    });

    console.log(`Servers( fetch status: ${r.r}): `, r.tool_servers)
    setFunctionList(r)
  } else {
    console.log(response.status)
  }
}

</script>


<style lang="scss">
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

html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, tt, var, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td {
    margin: 0;
    padding: 0;
    border: 0;
    font-weight: inherit;
    font-style: inherit;
    font-family: inherit;
    font-size: 100%;
    vertical-align: baseline;
}

a, div, span, strong, button, input, textarea, select, label {
    outline: 0;
}

</style>
