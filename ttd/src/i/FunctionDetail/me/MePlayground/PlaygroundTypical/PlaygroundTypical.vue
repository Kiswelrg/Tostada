<template>
    <div class="tooltypical z-[2] flex flex-col justify-between h-full w-full text-white">
        
        <div class="toolbody flex flex-col h-[calc(100%-53px)]">
            <PGHead :title="tool.title" :intro="tool.intro"/>
            <div class="belly overflow-y-auto">
                <div class="introduction">
                    <div class="introwrapper flex flex-col items-left text-center">
                        <div v-for="_ in 2" class="hidden">
                            <span class="text-sm text-left text-2s">小炒计算器(1)、clash config合成器(2+)、</span>
                            <span class="text-sm text-left text-2s">便利贴(big)</span>
                        </div>

                    </div>
                </div>
                <div class="toolmenu"></div>
                <div class="prompts">
                    <div class="prompt-wrapper text-left">

                    </div>
                </div>
            </div>
        </div>
        
        <InputKing />
    </div>

</template>

<script setup>
import InputKing from '@/i/Global/InputKing/InputKing.vue'
import PGHead from './PGHead/PGHead.vue'
import { ref } from 'vue'
const tool = ref({
    title: 'tool',
    intro: 'this is an introduction'
})
</script>

<style lang="scss" scoped>

</style>