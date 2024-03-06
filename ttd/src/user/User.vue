<template>
    <div class="main h-full w-full flex flex-col bg-white">
        <Header />
        <!-- Component changes when currentTab changes -->
        <div class="user-body flex h-full w-full justify-between">
            <div class="h-full"></div>
            <!-- <component :is="currentTab" class="text-black flex w-[300px] h-full">
            </component> -->
            <router-view class="text-black flex w-[300px] h-full">
            </router-view>
            <div class="h-full"></div>

        </div>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Header from './Header/Header.vue'

onMounted(() => {
    
})




</script>

<style lang="scss" setup>

</style>