<template>
    <div class="tooltypical h-full w-full text-white">
        <div class="toolhead w-full h-12">
            <div class="wrapper m-0 w-full h-full">
                <div class="flex flex-row px-4 py-3">
                    <div class="h-4 w-4 my-auto">
                        <img class="hashsvg h-full" src="@/assets/hashtag-solid.svg" alt="">
                    </div>
                    <div class="toolname text-start h-6 w-full pl-1 flex items-center">
                        <span class="text-xs/semibold text-white">Some Tool</span>
                    </div>
                    <div class="h-6 w-6">
                        <div class="dropdownarror h-5 w-5 relative mb-0 mr-0"></div>
                    </div>

                </div>
            </div>
        </div>

        <div class="toolbody">
            <div class="introduction">
                <div class="introwrapper flex flex-col items-left">
                    <span class="text-sm text-left">this is an introduction</span>
                    <span class="text-sm text-left text-2s">小炒计算器(1)、clash config合成器(2+)、</span>
                    <span class="text-sm text-left text-2s">云盘（1）</span>
                    
                </div>
            </div>
            <div class="toolmenu"></div>
            <InputKing></InputKing>
        </div>

    </div>

</template>

<script setup>
import InputKing from '@/../i/InputKing/InputKing.vue'
</script>

<style lang="scss" scoped>
.toolhead {
    box-shadow: 0 0 2px 0 rgba(0,0,0,0.5);
}

.hashsvg {
    filter: invert(100%) sepia(3%) saturate(7453%) hue-rotate(138deg) brightness(111%) contrast(104%);
}
</style>