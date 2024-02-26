<template>
  <!-- something else-->
  <div class="toollist h-full overflow-y-scroll">
      <div class="seomthingelse">
      </div>
      <div class="h-2 invisible"></div>
      <div v-for="(section,index) in sections" class="dm section text-hui-800 text-sm w-full min-h-10 text-left">
          <div v-if="!section.hiddenMenu" class="w-full bg-gray flex h-10 pt-[18px] pr-2 pb-1 pl-[18px] box-border text-ellipsis whitespace-nowrap overflow-hidden uppercase text-3s/[16px] tracking-[.02em] font-semibold">
              <span class="flex-1 overflow-hidden text-ellipsis outline-0">
                  {{ section.name }}
              </span>
              <div class="h-4 w-4 ml-0.5 mb-0 relative cursor-pointer outline-0 self-end">
                <img type="image/svg+xml" src="/static/tool/main/plus-solid.svg" alt="" class="svg-hui-800 mr-0.5 mb-0 h-3 w-3 cursor-pointer" />
              </div>
          </div>
          <div v-for="sub in section.subsec" :key="section.id" @click="selectSubSection(sub.id)" class="toolbutton text-white flex ml-3 mr-2 mb-0.5 p-1 hover:bg-hui-700 rounded" :class="{'bg-hui-700': selectedSubSection == sub.id}">
              <div class="h-6 w-6 my-auto mx-1">
                  <img class="h-6 w-6" :src="sub.logo" alt="" />
              </div>
              <div class="uppercase">
                  {{ sub.name }}
              </div>
              <div class=""></div>
              
          </div>
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const hashtag_url = '/static/tool/main/chevron-down-solid.svg'
const chevron_url = '/static/tool/main/hashtag-solid.svg'
let selectedSubSection = ref(-1)

const sections = ref([
{
  name:'Menu',
  hiddenMenu: true,
  subsec:[
      {
          name: 123124,
          id: 1,
          logo: '/static/@me/1F952.svg'
      },
      {
          name: 123124,
          id: 2,
          logo: '/static/@me/1F953.svg'
      },
      {
          name: 123124,
          id: 3,
          logo: '/static/@me/1F954.svg'
      }
  ]
},{
  name:'Direct Messeges',
  subsec:[
      {
          name: 123124,
          id: 12,
          logo: '/static/@me/1F955.svg'
      },
      {
          name: 123124,
          id: 23,
          logo: '/static/@me/1F956.svg'
      },
      {
          name: 123124,
          id: 34,
          logo: '/static/@me/1F957.svg'
      }
  ]
}
])

onMounted(()=>{
    
})

function selectSubSection(id) {
  selectedSubSection.value = id
}

function checkIsSelected(id) {
}

</script>

<style lang="scss" scoped>
.svg-hui-800 {
    filter: invert(53%) sepia(5%) saturate(576%) hue-rotate(189deg) brightness(97%) contrast(86%);
}

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