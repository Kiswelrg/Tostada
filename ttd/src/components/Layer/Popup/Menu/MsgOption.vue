<template>
    <div class="menu relative flex min-w-[188px] max-w-[320px] h-auto cursor-default max-h-[calc(100vh-32px)] rounded-[4px] bg-[var(--background-floating)] shadow-[var(--shadow-high)] z-10">
        <div class="relative text-white scroller px-2 py-1.5 flex-auto">
            <div class="group grid pt-1 pr-[1px] pb-1.5 pl-[1px] h-auto grid-cols-4 grid-rows-[1fr] items-center justify-items-center outline-0">
                <div v-for="i in 4" :key="i" class="customItem text-[var(--interactive-normal)] border-[var(--interactive-normal)] text-[14px] font-medium leading-[18px]">
                    <div class="button flex items-center justify-center w-8 h-8 p-1 cursor-pointer rounded-[50%] bg-[var(--background-tertiary)]"></div>
                </div>
                
            </div>
            <div class="group">
                <item
                    v-for="(item, index) in options"
                    :key="index"
                    class="flex min-h-8 items-center px-2 py-1.5 justify-between mx-0 my-0.5 rounded-[2px] text-[13px] font-medium leading-[18px] cursor-pointer outline-0 text-[var(--interactive-normal)] border-[var(--interactive-normal)] text-left">
                    <div class="label relative flex-auto whitespace-nowrap overflow-hidden text-ellipsis outline-0">{{ item }}</div>
                    <div class="iconContainer relative h-[18px] w-[18px] flex-auto grow-0 shrink-0 ml-2 outline-0">
                        <font-awesome-icon :icon="['fas', 'arrow-left']"
                                            class="block h-[18px] w-[18px] object-contain" />
                    </div>
                </item>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const options = ref([
    'Edit Message',
    'Copy Text',
    'Copy Message Link',
    'Delete Message',
])

</script>

<style lang="scss">

</style>

<style lang="scss" scoped>

</style>