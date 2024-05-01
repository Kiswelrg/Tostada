<template>
    <div>
    <div class="toollist h-[calc(100vh-var(--m-serverhead-height)-var(--m-userbar-height))] overflow-y-scroll">
        <div class="somethingelse">
        </div>

        <div 
          v-for="(section, index) in orderedSD" 
          :key="index" 
          class="section text-hui-800 text-sm w-full min-h-10 pt-0"
          @dragenter.prevent
          @dragover.prevent
          >
          <div class="w-full bg-gray flex pt-4"
            draggable="true"
            @drop.prevent="onDropCategory($event, section.cid)"
            @dragstart="startDragCategory($event, section.cid)">
              <div class="h-2 w-2 my-auto mx-1">
                  <img class="downsvg" :src="hashtag_url" alt="" />
              </div>
              <div class="uppercase text-[11px]">
                  {{ section.name }}
              </div>
              <div class=""></div>
          </div>
          <div 
            v-for="sub in section.tools" 
            :key="sub.cid" 
            @click="selectSubSection(sub)" 
            class="toolbutton text-white flex ml-3 mr-2 p-1 mb-0.5 rounded" 
            :class="{'bg-hui-700': selectedSubSection == sub.cid, 
            'hover:bg-hui-500': selectedSubSection != sub.cid}"
            @dragenter.prevent
            @dragover.prevent
            @drop.prevent="onDrop2Tool($event, -1, index+1 === orderedSD.length)">
              <div class="h-2 w-2 my-auto mx-1">
                  <img class="hashsvg" :src="chevron_url" alt="" />
              </div>
              <div class="uppercase text-[10px]">
                  {{ sub.name }}
              </div>
              <div class=""></div>
              
          </div>
        </div>
    </div>
    </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { inject, onMounted, onUnmounted } from 'vue';
import { watch } from 'vue';
import { useWatchOnce } from '@/util/watcher'
import { jsonWithBigInt } from '@/util/parse';
import { getCookie } from '@/util/session';
const server = inject('active-server')
const hashtag_url = '/static/tool/main/chevron-down-solid.svg'
const chevron_url = '/static/tool/main/hashtag-solid.svg'
const emit = defineEmits([
    'select-tool'
])
let selectedSubSection = ref(-1)
const server_detail = ref([])


function selectSubSection(obj) {
  selectedSubSection.value = obj.cid;
  emit('select-tool', obj);
}


onMounted(() => {
    (async () => {
        
    })();
})

const watcher_server = watch(server, async (newQuestion, oldQuestion) => {
    if (!server || !server.value) {
      return;
    }
    await fetchAToolServer(server.value.cid);
    
}, { immediate: true})


const { stopped, stopWatcher } = useWatchOnce(server_detail,
  (newValue, old) => {
    if (Array.isArray(newValue) && newValue.length > 0) {
      for (let entry of newValue) {
        for (const [key, val] of Object.entries(entry.tools)) {
          if (!val) continue
          selectSubSection(val)
          return true
        }
      }
    }
    return false
  }
)


function setDefaultTool() {
    for (let entry of server_detail.value) {
        for (const [key, val] of Object.entries(entry.tools)) {
            if (!val) continue
            selectSubSection(val)
            return;
        }
    }
    return;
}


const startDragCategory = (e, cid) => {
  // var d = new Date(server.date_added)
  // console.log(e.target, server, d)
  e.dataTransfer.dropEffect = 'move'
  e.dataTransfer.effectAllowed = 'move'
  e.dataTransfer.setData('cid', cid)
}

const onDragOver = (e) => {
  console.log('dragging')
}

const onDrop2Tool = (e, cid, isTheLast) => {
  if (isTheLast) onDropCategory(e, cid)
}

const onDropCategory = (e, cid) => {
  const startCID = BigInt(e.dataTransfer.getData('cid'))
  const onself = cid == startCID
  if (onself) return
  const oldIndex = orderedSD.value.findIndex(obj => obj.cid === startCID)
  const newIndex = cid === -1 ? orderedSD.value.length : orderedSD.value.findIndex(obj => obj.cid === cid)
  // postion does not change.
  if (oldIndex + 1 === newIndex) return

  const r = reorderCategorys(orderedSD.value, oldIndex, newIndex)
  submitOrderChange(r)
}



const reorderCategorys = (sd, oldIndex, newIndex) => {
  const clone = (ele) => {
    return {
      'cid': ele.cid,
      'order': ele.order,
      'name': ele.name
    }
  }

  let r = []
  let curIdx = 0
  let skipped = 0
  for (let i = 0; i < sd.length; i++) {
    if (i === oldIndex) {
      continue
    } else if (i === newIndex) {
      if (sd[oldIndex].order !== curIdx + 1) {
        r.push(clone(sd[oldIndex]))
        r.at(-1).order = curIdx + 1
        r.at(-1).old_order = sd[oldIndex].order
        ++skipped
      }
      ++curIdx
      if (sd[newIndex].order !== curIdx + 1) {
        r.push(clone(sd[newIndex]))
        r.at(-1).order = curIdx + 1
        r.at(-1).old_order = sd[newIndex].order
        ++skipped
      }
      ++curIdx
    } else {
      if (sd[i].order !== curIdx + 1) {
        r.push(clone(sd[i]))
        r.at(-1).order = curIdx + 1
        r.at(-1).old_order = sd[i].order
        ++skipped
      }
      ++curIdx
    }
  }
  if(newIndex == sd.length) {
    r.push(clone(sd[oldIndex]))
    r.at(-1).order = curIdx + 1
    r.at(-1).old_order = sd[oldIndex].order
  }
  return r
}

const updateCategoryOffline = (r, use_old) => {
  server_detail.value.map((category) => {
    const c_in_s = r.find(obj => obj.cid === category.cid)
    if (!c_in_s) return category
    category.order = use_old ? c_in_s.old_order : c_in_s.order
    return category
  })
}

function setServerDetail(r) {
    server_detail.value = []
    if (!('category' in r['tool_server'])) return
    for (const [k, v] of Object.entries(r['tool_server']['category'])) {
        server_detail.value.push({
            name: k,
            type: v['tools'][0]['category']['type'],
            tools: v['tools'],
            order: v['order'],
            cid: BigInt(v['cid']),
        })
    }
}


const orderedSD = computed(() => {
  if (!server_detail.value || !server_detail.value.length) return []
  return server_detail.value.toSorted((a, b) => {
    const orderdiff = a.order - b.order
    return orderdiff === 0 ? a.name.localeCompare(b.name) : orderdiff
  })
})


async function fetchAToolServer(cid) {
  const response = await fetch(
    `/api/i/tool_server/${cid}/?tools=1`,
    {
      method: "GET",
    }
  )
  
  const t = await response.text()
  if (response.ok) {
    const r = JSON.parse(t)
    console.log(`Server (fetch status: ${r.r}): `, r)
    setServerDetail(r)
  } else {
    console.log(response.status)
  }
}

const submitOrderChange = async (r) => {
  // Apply order change anyway
  updateCategoryOffline(r, false)

  // After the server responded, change again if failed.
  var form_data = new FormData()
  form_data.append('change_list', JSON.stringify(r.map((obj) => {
    return {
      'cid': obj.cid.toString(),
      'order': obj.order,
      'name': obj.name,
      'old_order': obj.old_order,
    }
  })))

  const response = await fetch(
    `/api/i/reordersc/`,
    {
      method: "POST",
      body: form_data,
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      }
    }
  )
  
  const text = await response.text()
  if (response.ok) {
    const r = jsonWithBigInt(text)
    // console.log(`Reorder Sc (result: ${r.r}): `, r)

  } else {
    console.log(response.status)
    updateCategoryOffline(r, true)
    // Replace the current page content with the fetched HTML
    document.open();
    document.write(text);
    document.close();
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