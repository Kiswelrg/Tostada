<template>
    <div>
    <div class="toollist h-full overflow-y-scroll">
        <div class="seomthingelse">
        </div>

        <div v-for="(section,index) in server_detail" class="section text-hui-800 text-sm w-full min-h-10 pt-4">
            <div class="w-full bg-gray flex">
                <div class="h-2 w-2 my-auto mx-1">
                    <img class="downsvg" :src="hashtag_url" alt="" />
                </div>
                <div class="uppercase">
                    {{ section.name }}
                </div>
                <div class=""></div>
            </div>
            <div v-for="sub in section.tools" :key="sub.cid" @click="selectSubSection(sub.cid)" class="toolbutton text-white flex ml-3 mr-2 p-1 hover:bg-hui-700 rounded" :class="{'bg-hui-700': selectedSubSection == sub.cid}">
                <div class="h-2 w-2 my-auto mx-1">
                    <img class="hashsvg" :src="chevron_url" alt="" />
                </div>
                <div class="uppercase">
                    {{ sub.name }}
                </div>
                <div class=""></div>
                
            </div>
        </div>
    </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { inject, onMounted } from 'vue';
import { watch } from 'vue';

const server = inject('active-server')
const hashtag_url = '/static/tool/main/chevron-down-solid.svg'
const chevron_url = '/static/tool/main/hashtag-solid.svg'
let selectedSubSection = ref(-1)
const server_detail = ref([
  {
    name:'Loading',
    subsec:[
        {
            name: 1,
            id: 1
        }
    ]
  }
])

onMounted(() => {
    (async () => {
        
    })();
})

watch(server, async (newQuestion, oldQuestion) => {
    if (!server || !server.value) {
        console.log('loading server detail!');
        return;
    }
    await fetchAToolServer(server.value.cid);
})

function setServerDetail(r) {
    server_detail.value = [];
    if (!('category' in r['tool_server'])) return;
    for (const [k, v] of Object.entries(r['tool_server']['category'])) {
        server_detail.value.push({
            name: k,
            type: v[0]['category']['type'],
            tools: v
        });
    }
}

function selectSubSection(id) {
    selectedSubSection.value = id
}

async function fetchAToolServer(cid) {
  const response = await fetch(
    `/api/i/tool_server/${cid}/?tools=1`,
    {
      method: "GET",
    }
  );
  
  if (response.ok) {
    const r = await response.json();
    setServerDetail(r);
  } else {
    console.log(response.status);
  }
}

</script>

<style lang="scss" scoped>
.toollist {
    
    &::-webkit-scrollbar {
        background-color: transparent;
        width: 8px;
        height: 100%;
    }
    &::-webkit-scrollbar-thumb {
        background-color: rgb(27, 27, 27);
        // border: 4px solid #2b2d31;
        border: 2px solid rgba(0,0,0,0);
        background-clip: padding-box;
        border-radius: 4px;
    }
    
}
.downsvg, .hashsvg {
    filter: invert(100%) sepia(3%) saturate(7453%) hue-rotate(138deg) brightness(111%) contrast(104%);
}


</style>