<template>

  <div class="functionlist bg-fclist-bg flex flex-col flex-none h-screen overflow-y-scroll w-full">
    <!-- Direct Message icons -->
    <div class="sublist flex-1 mx-0 grow-0">
      <div class="flex flex-col w-full">
        <div class="functioner h-12 w-full relative flex mx-0 mt-0 mb-2 justify-center"
             @click="GoMe"
             v-for="(message, index) in props.functionList.directMessages"
             :key="index">
          <div>

          </div>
          <!-- Your direct message icons here -->
          <span class="icon inline-block relative w-12 h-12 bg-[#313338] rounded-full hover:rounded-2xl">
            <img :src="message.logoSrc"
                 alt="Direct Message"
                 class="icon cursor-pointer mx-auto w-full h-full z-10 transitionduration-300 ease-in-out rounded-full scale-[0.6]" @dragstart.prevent/>
            <div class="absolute hidden z-0 w-full h-full top-0 left-0 bg-[#313338] rounded-full hover:rounded-2xl">
            </div>
          </span>
        </div>
      </div>
    </div>

    <div>
      <div class="delimeter h-0.5 w-8 flex-1 mx-auto mb-2">

      </div>
    </div>

    <!-- User's joined servers icons -->
    <div class="sublist flex-1 mx-0 grow-0 w-full">
      <div class="flex flex-col w-full">

        <div class="functioner h-12 w-full relative flex mx-0 mt-0 mb-2 justify-center"
             @click="clickFunctioner($event, server.cid)"
             v-for="(server, index) in orderedServers"
             :key="index"
             :id="'functioner_' + server.cid"
             @dragenter.prevent
             @dragover.prevent
             @drop.prevent="onDropServer($event, server.cid)">
          <div class="absolute w-0.5 h-2 white block left-0 inset-y-auto">
          </div>
          <!-- Your joined servers icons here -->
          <span class="icon inline-block w-12 h-12">
            <img :src="server.logoSrc + '?size=256'"
                 alt="Server"
                 class="icon cursor-pointer relative m-full h-full mx-auto rounded-full hover:rounded-2xl transition duration-300 ease-in-out"
                 draggable="true"
                 @dragstart="startDragServer($event, server.cid)" />
          </span>
          <div
               class="drag-mask absolute flex items-stretch flex-col -top-4 -bottom-1 left-0 right-0 pointer-events-none">
            <div class="above-block flex-1"
                 :id="'above_' + server.cid"
                 :cid="server.cid"></div>
            <div class="combine-block flex-1"
                 :id="'combine_' + server.cid"
                 :cid="server.cid"></div>
          </div>
        </div>

        <div class="functioner h-12 w-full relative flex mx-0 mt-0 mb-2 justify-center"
             v-for="(server, index) in props.functionList.serverButtons"
             :key="index"
             :id="'functioner_' + server.cid"
             @dragenter.prevent
             @dragover.prevent
             @drop.prevent="onDropServer($event, -1)">
          <div class="absolute w-0.5 h-2 white block left-0 inset-y-auto">
          </div>
          <!-- Your 2-buttons here -->
          <span class="icon inline-block w-12 h-12 bg-text-muted rounded-full">
            <img :src="server.logoSrc"
                 alt="Server"
                 class="icon cursor-pointer relative m-full h-full mx-auto rounded-full hover:rounded-2xl transition duration-300 ease-in-out"
                 :style="serverScale(server)"
                 draggable="true"
                 @dragstart.prevent />
          </span>
          <div
               class="drag-mask absolute flex items-stretch flex-col -top-4 -bottom-1 left-0 right-0 pointer-events-none">
            <div class="above-block flex-1"
                 :id="'above_' + server.cid"
                 :cid="server.cid"></div>
            <div class="combine-block flex-1"
                 :id="'combine_' + server.cid"
                 :cid="server.cid"></div>
          </div>
        </div>

      </div>
    </div>

    <!-- Find Server Button -->
    <div>
      <div class="delimeter h-0.5 w-8 flex-1 mx-auto mb-2">

      </div>
    </div>

    <!-- Placeholder icons -->
    <div class="sublist flex-1 mx-0 grow-0">
      <div class="flex flex-col w-full">
        <div class="functioner h-12 w-full relative flex mx-0 mt-0 mb-2 justify-center"
             v-for="(func, index) in props.functionList.placeholderCount"
             :key="index">
          <!-- Your placeholder icons here -->
          <span class="icon inline-block w-12">
            <img @click="GoHome"
                 :src="func.logoSrc"
                 alt="Others"
                 @dragstart.prevent
                 class="icon cursor-pointer relative mx-auto rounded-full hover:rounded-2xl transition duration-300 ease-in-out" />
          </span>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router';
import { getCookie } from '@/util/session';
import { jsonWithBigInt } from '@/util/parse';
const route = useRoute();

const props = defineProps({
    functionList: Object,
})


const emit = defineEmits(
  [
    'update-active-server-tab',
    'go-tab',
    'updateServerList',
    'updateServerListOffline',
  ]
)

onMounted(() => {
  (async () => {
    // await fetchServers();
  })();
  
});

const serverScale = (s) => {
  if(!s || ! 'scale' in s) return {}
  return {
    'scale': s.scale
  }
}

const ogServers = computed(() => {
  return props.functionList.joinedServers
})

const orderedServers = computed(() => {
  if (!props.functionList) return []
  return props.functionList.joinedServers.toSorted((a, b) => {
    if (a.order !== b.order) return a.order - b.order
    else {
      let date1 = new Date(a.date_added)
      let date2 = new Date(b.date_added)
      return date1 - date2
    }
  })
  
})


const startDragServer = (e, cid) => {
  // var d = new Date(server.date_added)
  // console.log(e.target, server, d)
  e.dataTransfer.dropEffect = 'move'
  e.dataTransfer.effectAllowed = 'move'
  e.dataTransfer.setData('cid', cid)
}

const onDragOverFL = (e) => {
  console.log('dragging')
}

const reorderServers = (ss, oldIndex, newIndex) => {
  const clone = (ele) => {
    return {
      'cid': ele.cid,
      'order': ele.order,
      'date_added': ele.date_added
    }
  }

  let r = [];
  let curIdx = 0;
  let skipped = 0;
  for (let i = 0; i < ss.length; i++) {
    if (i === oldIndex) {
      continue;
    } else if (i === newIndex) {
      if (ss[oldIndex].order !== curIdx + 1) {
        r.push(clone(ss[oldIndex]));
        r.at(-1).order = curIdx + 1;
        r.at(-1).old_order = ss[oldIndex].order;
        ++skipped;
      }
      ++curIdx;
      if (ss[newIndex].order !== curIdx + 1) {
        r.push(clone(ss[newIndex]));
        r.at(-1).order = curIdx + 1;
        r.at(-1).old_order = ss[newIndex].order;
        ++skipped;
      }
      ++curIdx;
    } else {
      if (ss[i].order !== curIdx + 1) {
        r.push(clone(ss[i]));
        r.at(-1).order = curIdx + 1;
        r.at(-1).old_order = ss[i].order;
        ++skipped;
      }
      ++curIdx;
    }
  }
  if(newIndex == ss.length) {
    r.push(clone(ss[oldIndex]))
    r.at(-1).order = curIdx + 1;
    r.at(-1).old_order = ss[oldIndex].order;
  }
  return r;
};

const submitOrderChange = async (r) => {
  // Apply order change anyway
  emit('updateServerListOffline', r, false)

  // After the server responded, change again if failed.
  var form_data = new FormData()
  form_data.append('change_list', JSON.stringify(r.map((obj) => {
    return {
      'cid': obj.cid.toString(),
      'order': obj.order,
      'date_added': obj.date_added,
      'old_order': obj.old_order,
    }
  })))

  const response = await fetch(
    `/api/i/reorderss/`,
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
    // console.log(`Reorder Ss (result: ${r.r}): `, r)
   
    // Legacy Implement!
    // emit('updateServerList')
  } else {
    console.log(response.status)
    emit('updateServerListOffline', r, true)
    // Replace the current page content with the fetched HTML
    document.open();
    document.write(text);
    document.close();
  }
}

const onDropServer = (e, cid) => {
  const startCID = BigInt(e.dataTransfer.getData('cid'))
  const onself = cid == startCID
  // above
  const within = (block, x, y) => {
    if (
      (x >= block.x && x < block.x + block.width) &&
      (y >= block.y && y < block.y + block.height)
    ) return true
    return false
  }
  // const ss = strippedServers.value
  const oldIndex = orderedServers.value.findIndex(obj => obj.cid === startCID)
  const newIndex = orderedServers.value.findIndex(obj => obj.cid === cid)
  if(cid === -1) {
    if(oldIndex + 1 === orderedServers.value.length) return
    const r = reorderServers(orderedServers.value, oldIndex, orderedServers.value.length)
    submitOrderChange(r)
    return
  }
  const parent = document.getElementById('functioner_' + cid)
  const aboveB = parent.querySelector('.above-block').getBoundingClientRect()
  const combineB = parent.querySelector('.combine-block').getBoundingClientRect()
  if (!onself && within(aboveB, e.clientX, e.clientY)) {
    if (oldIndex + 1 === newIndex) return
    const r = reorderServers(orderedServers.value, oldIndex, newIndex)
    submitOrderChange(r)
  }
  else if (!onself && within(combineB, e.clientX, e.clientY)) {
    console.log('should combine')
  }
}

function GoHome(){
    window.location.href = '/'
}
function GoMe(){
  emit('go-tab', '/i/@me')
}
function GoChannel(){
  emit('go-tab', '/i')
}

function clickFunctioner(e, cid){
  // If special do not go
  GoChannel()

  // Emit
  emit('update-active-server-tab', cid)
}

const watcher_orderedServers = watch(ogServers, async (newS, oldS) => {
    if (!orderedServers.value) {
      console.log(orderedServers.value)
      return
    }
    if (orderedServers.value.length) {
      emit('update-active-server-tab', orderedServers.value[0].cid)
    }
}, { immediate: true})

</script>

<style scoped lang="scss">
.main {
  height: 100%;

  .functionlist {
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

  .functionlist::-webkit-scrollbar {
    display: none;
  }

}


</style>
