<template>
    <div class="main h-full w-full flex flex-col bg-white">
        <Header />
        <!-- Component changes when currentTab changes -->
        <keep-alive>
            <component :is="currentTab" class="text-black grow"></component>
        
        </keep-alive>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, defineProps } from 'vue'
import Header from './Header/Header.vue'
import Home from './Home/Home.vue'
import Login from './Login/Login.vue'
import Signup from './Signup/Signup.vue'

const p = defineProps({
    currentTabIndex: Number
})

const currentTabIndex = ref(p.currentTabIndex)

const tabs = ref(
    [
        Home,
        Login,
        Signup,
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