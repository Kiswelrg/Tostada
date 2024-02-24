<template>
    <div class="main h-full w-full flex flex-col bg-white">
        <Header />
        <!-- Component changes when currentTab changes -->
        <div class="user-body flex h-full w-full justify-between">
            <div class="h-full"></div>
            <!-- <router-view :is="currentTab" class="text-black flex w-[300px] h-full">
            </router-view> -->
            <Empty helloText="All the Tools You Need, Are Here"></Empty>
            <div class="h-full"></div>

        </div>
        
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Header from '@/user/Header/Header.vue'
import Home from '@/user/Home/Home.vue'
import Empty from '../components/Util/Empty.vue'

const p = defineProps({
    currentTabIndex: Number
})

const currentTabIndex = ref(p.currentTabIndex)

const tabs = ref(
    [
        Home,
    ]
)

const currentTab = computed(() => {
    if(p.currentTabIndex == undefined)
        p.currentTabIndex = 0
    return tabs.value[currentTabIndex.value]
})

onMounted(() => {
    console.log('User Page')
})




</script>

<style lang="scss" setup>

</style>