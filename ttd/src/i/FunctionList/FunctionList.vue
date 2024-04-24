<template>

  <div 
    class="functionlist bg-fclist-bg flex flex-col flex-none h-screen overflow-y-scroll w-full"
    
    >
    <!-- Direct Message icons -->
    <div class="sublist flex-1 mx-0 grow-0">
      <div class="flex flex-col w-full">
        <div class="functioner h-12 w-full relative flex mx-0 mt-0 mb-2 justify-center"
             @click="GoMe"
             v-for="(message, index) in functionList.directMessages"
             :key="index">
          <div>

          </div>
          <!-- Your direct message icons here -->
          <span class="icon inline-block relative w-12 h-12 bg-[#313338] rounded-full hover:rounded-2xl">
            <img :src="message.logoSrc"
                 alt="Direct Message"
                 class="icon mx-auto w-full h-full z-10 transitionduration-300 ease-in-out rounded-full scale-[0.6]" />
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
             v-for="(server, index) in functionList.joinedServers"
             :key="index">
          <div class="absolute w-0.5 h-2 white block left-0 inset-y-auto">
          </div>
          <!-- Your joined servers icons here -->
          <span class="icon inline-block w-12 h-12">
            <img :src="server.logoSrc"
                 alt="Server"
                 class="icon relative m-full h-full mx-auto rounded-full hover:rounded-2xl transition duration-300 ease-in-out" 
                 draggable="true"
                 @dragstart="startDragServer($event, server)"/>
          </span>
          <div class="drag-mask absolute flex items-stretch flex-col -top-4 -bottom-1 left-0 right-0 pointer-events-none bg-[color:#8a67673b] z-10">
            <div class="above" :id="'above_' + server.name" :cid="server.cid" @drop.prevent="onDropServer($event)"></div>
            <div class="combine" :id="'combine_' + server.name" :cid="server.cid" @drop.prevent="onDropServer($event)"></div>
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
             v-for="(func, index) in functionList.placeholderCount"
             :key="index">
          <!-- Your placeholder icons here -->
          <span class="icon inline-block w-12">
            <img @click="GoHome"
                 :src="func.logoSrc"
                 alt="Others"
                 class="icon cursor-pointer relative mx-auto rounded-full hover:rounded-2xl transition duration-300 ease-in-out" />
          </span>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router';
const route = useRoute();

const props = defineProps({
    functionList: Object,
})

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

const startDragServer = (e, server) => {
  var d = new Date(server.date_added)
  // console.log(e.target, server, d)
}

const onDragOverFL = (e) => {
  // console.log(e.target)
  console.log('dragging')
}

const onDropServer = (e) => {
  // console.log(e.target)
  console.log('dropped')
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
