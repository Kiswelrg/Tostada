<template>
    <!-- something else-->
    <div class="">
        <div class="seomthingelse">

        </div>

        <div v-for="(section,index) in sections" class="section text-hui-800 text-sm w-full min-h-10 pt-4">
            <div class="w-full bg-gray flex">
                <div class="h-2 w-2 my-auto mx-1">
                    <img class="downsvg" src="@/assets/chevron-down-solid.svg" alt="" />
                </div>
                <div class="uppercase">
                    {{ section.name }}
                </div>
                <div class=""></div>
            </div>
            <div v-for="sub in section.subsec" :key="section.id" @click="selectSubSection(sub.id)" class="toolbutton text-white flex ml-3 mr-2 p-1 hover:bg-hui-700 rounded" :class="{'bg-hui-700': selectedSubSection == sub.id}">
                <div class="h-2 w-2 my-auto mx-1">
                    <img class="hashsvg" src="@/assets/hashtag-solid.svg" alt="" />
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
import {ref} from 'vue'
let selectedSubSection = ref(-1)
const sections = ref([
  {
    name:'asd',
    subsec:[
        {
            name: 123124,
            id: 1
        },
        {
            name: 123124,
            id: 2
        },
        {
            name: 123124,
            id: 3
        }
    ]
  },{
    name:'adsfag',
    subsec:[
        {
            name: 123124,
            id: 12
        },
        {
            name: 123124,
            id: 23
        },
        {
            name: 123124,
            id: 34
        }
    ]
  }
])

function selectSubSection(id) {
    selectedSubSection.value = id
}

function checkIsSelected(id) {
}

</script>

<style lang="scss" scoped>

.downsvg, .hashsvg {
    filter: invert(100%) sepia(3%) saturate(7453%) hue-rotate(138deg) brightness(111%) contrast(104%);
}


</style>