<template>
<div class="serverhead w-full h-12">
    
    <div class="wrapper m-0 w-full h-full">
        <div class="flex flex-row px-4 py-3">
            <div class="h-6 w-6 my-auto">
                <img class="h-full" :src="thumb_url" alt="">
            </div>
            <div class="servername text-start h-6 w-full pl-1">
                <span class="text-xs text-white truncate">Some Server</span>
            </div>
            <div class="h-6 w-6">
                <div class="dropdownarror h-5 w-5 relative mb-0 mr-0"></div>
            </div>
            
            <!-- someting else-->
            <div class="some thing else"></div>
        </div>
    </div>

    <!-- someting else-->
    <div class="wrapper"></div>
</div>
</template>

<script setup>
import { ref } from 'vue';
const thumb_url = '/ipa/tool/main/thumb.svg';

</script>

<style lang="scss" scoped>
.serverhead {
    box-shadow: 0 0 2px 0 rgba(0,0,0,0.5);
}

.dropdownarror {
    &::before,&::after {
        content: "";
        position: absolute;
        width: 2px; /* Adjust the width of the pillars */
        height: 8px;
        background-color: white; /* Adjust the color of the pillars */
        top: 50%;
        border-radius: 3px;
    }
    &::before {
        right: 22%;
        transform: rotate(-45deg);
    }
    &::after {
        right: 0;
        transform: rotate(45deg);
    }
}
</style>