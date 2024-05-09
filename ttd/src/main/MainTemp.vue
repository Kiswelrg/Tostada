<template>
    <div class="main h-full w-full flex flex-col bg-white">
        <Header />
        <!-- Component changes when currentTab changes -->
        <div class="user-body flex h-full w-full justify-between">
            <div class="h-full"></div>
            <Empty helloText="All the tools you need, are here"></Empty>
            <div class="h-full"></div>

        </div>
        
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Header from '@/account/Header/Header.vue'
import Home from '@/account/Home/Home.vue'
import Empty from '../components/Util/Empty.vue'

const p = defineProps({
    currentTabIndex: Number
})

const helloHTML = ref(`<div class="flex items-center h-full mx-1 shrink-0 rounded-sm">All the 
                <a href="/i/"
                   type="button"
                   class="button inline-block rounded bg-neutral-50 px-6 pb-2 pt-2.5 text-[11px] font-medium uppercase leading-normal text-neutral-800 shadow-[0_4px_9px_-4px_#cbcbcb] transition duration-150 ease-in-out hover:bg-neutral-100 hover:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] focus:bg-neutral-100 focus:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] focus:outline-none focus:ring-0 active:bg-neutral-200 active:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] dark:hover:shadow-[0_4px_9px_-4px_rgba(251,251,251,0.3)] dark:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] dark:focus:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] dark:active:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] bg-white text-[#000000]">
                    Tools
                </a> You Need, Are Here
            </div>`)

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