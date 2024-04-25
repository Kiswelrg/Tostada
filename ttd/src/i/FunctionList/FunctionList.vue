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
                 class="icon mx-auto w-full h-full z-10 transitionduration-300 ease-in-out rounded-full scale-[0.6]" @dragstart.prevent/>
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
             @click="clickFunctioner($event, index)"
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
            <img :src="server.logoSrc"
                 alt="Server"
                 class="icon relative m-full h-full mx-auto rounded-full hover:rounded-2xl transition duration-300 ease-in-out"
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
             @click="clickFunctioner($event, index)"
             v-for="(server, index) in props.functionList.serverButtons"
             :key="index"
             :id="'functioner_' + server.cid"
             @dragenter.prevent
             @dragover.prevent
             @drop.prevent="onDropServer($event, -1)">
          <div class="absolute w-0.5 h-2 white block left-0 inset-y-auto">
          </div>
          <!-- Your joined servers icons here -->
          <span class="icon inline-block w-12 h-12">
            <img :src="server.logoSrc"
                 alt="Server"
                 class="icon relative m-full h-full mx-auto rounded-full hover:rounded-2xl transition duration-300 ease-in-out"
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
import { computed, onMounted, ref, toRaw } from 'vue'
import { useRoute } from 'vue-router';
const route = useRoute();

const props = defineProps({
    functionList: Object,
})

const functionListRef = ref(props.functionList)


const emit = defineEmits(
  [
    'update-active-server-tab',
    'go-tab'
  ]
)

onMounted(() => {
  (async () => {
    // await fetchToolServers();
  })();
  
});

const serverScale = (s) => {
  if(!s || ! 'scale' in s) return {}
  return {
    'scale': s.scale
  }
}

const orderedServers = computed(() => {
  if (!functionListRef.value) return []
  return functionListRef.value.joinedServers.toSorted((a, b) => {
    if (a.order !== b.order) return a.order - b.order
    else {
      let date1 = new Date(a.date_added)
      let date2 = new Date(b.date_added)
      return date1 - date2
    }
  })
  
})

const displayedServers = computed(() => {
  if (!functionListRef.value) return []
  return orderedServers.value.concat(functionListRef.value.serverButtons)
})


const strippedServers = computed(() => {
  let keep_list = [
    'name',
    'order',
    'date_added',
    'cid'
  ];
  let r = [];
  for (const s of orderedServers.value) {
    let strippedServer = {};
    for (const attribute of keep_list) {
      strippedServer[attribute] = s[attribute];
    }
    r.push(strippedServer);
  }
  return r;
});


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
      'name': ele.name,
      'cid': ele.cid,
      'order': ele.order,
      'date_added': ele.date_added
    }
  }

  let r = [];
  let curIdx = 0;
  let inserted = false;
  
  for (let i = 0; i < ss.length; i++) {
    if (i === oldIndex) {
      continue;
    } else if (i === newIndex) {
      r.push(clone(ss[oldIndex]));
      r[curIdx].order = ++curIdx;
      r.push(clone(ss[newIndex]));
      r[curIdx].order = ++curIdx;
    } else {
      r.push(clone(ss[i]));
      r[curIdx].order = ++curIdx;
    }
  }
  if(newIndex == ss.length) {
    r.push(clone(ss[oldIndex]))
    r[curIdx].order = ++curIdx;
  }
  return r;
};

const submitOrderChange = () => {
  console.log('submitting...')
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
  if(cid === -1) {
    const r = reorderServers(orderedServers.value, orderedServers.value.findIndex(obj => obj.cid === startCID), orderedServers.value.length)
    for (const s of r) {
      console.log(s.order, s.name, s.date_added)
    }
    submitOrderChange(r)
    return
  }
  const parent = document.getElementById('functioner_' + cid)
  const aboveB = parent.querySelector('.above-block').getBoundingClientRect()
  const combineB = parent.querySelector('.combine-block').getBoundingClientRect()
  if (!onself && within(aboveB, e.clientX, e.clientY)) {
    console.log('should put above')
    const ss = strippedServers.value
    const oldIndex = ss.findIndex(obj => obj.cid === startCID)
    const newIndex = ss.findIndex(obj => obj.cid === cid)

    for (const s of ss) {
      console.log(s.order, s.name, s.date_added)
    }
    
    console.log(oldIndex, newIndex)

    console.log('starting re-orderring...')

    const newOrderedServers = reorderServers(orderedServers.value, oldIndex, newIndex)
    console.log(newOrderedServers)
    for (const s of newOrderedServers) {
      console.log(s.order, s.name, s.date_added)
    }
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
function GoTool(){
  emit('go-tab', '/i')
}

function clickFunctioner(e, index){
  // If special do not go
  GoTool()

  // Emit
  emit('update-active-server-tab', index)
}

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
