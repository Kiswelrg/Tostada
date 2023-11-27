<template>
    <div class="tooltypical flex flex-col justify-between h-full w-full text-white">
        
        <div class="toolbody">
            <ToolHead :title="tool.title" :intro="tool.intro"/>
            <div class="introduction">
                <div class="introwrapper flex flex-col items-left">
                    <span class="text-sm text-left text-2s">小炒计算器(1)、clash config合成器(2+)、</span>
                    <span class="text-sm text-left text-2s">便利贴</span>

                </div>
            </div>
            <div class="toolmenu"></div>
        </div>
        
        <InputKing />
    </div>

</template>

<script setup>
import InputKing from '@/../i/Global/InputKing/InputKing.vue'
import ToolHead from '../ToolHead/ToolHead.vue'
import { ref } from 'vue'
const tool = ref({
    title: 'tool',
    intro: 'this is an introduction'
})
</script>

<style lang="scss" scoped>

</style>