<template>
    <div class="toolhead w-full h-12 flex items-center">
        <div class="toolinfo flex m-0 h-8 w-full items-center">
            <div class="tooltitle flex flex-row pl-4">
                <div class="h-4 w-4 my-auto">
                    <img class="hashsvg h-full" :src="hashtag_url" alt="">
                </div>
                <div class="toolname text-start h-6 w-full pl-1 flex items-center">
                    <span class="text-[11px] text-semibold text-white">{{ title }}</span>
                </div>
                

            </div>
            <div class="h-full my-auto flex">
                <div class="delimeter my-auto mx-2 w-[1px] h-6 bg-delimeter-toolhead"></div>
            </div>
            <div class="toolintro flex">
                <div class="toolname text-start h-6 w-full pl-1 flex items-center">
                    <span class="text-[9px] font-semibold text-[#adadad]">{{ intro }}</span>
                </div>
            </div>
        </div>

        <ToolBarTR 
            ref="toolBarTRRef"
            :tool-detail="toolDetail"
            @search-results="handleSearchResults"
            @search-cleared="handleSearchCleared"
            @search-focused="handleSearchFocused" />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import ToolBarTR from '@/i/Global/ToolBarTR/ToolBarTR.vue'
const hashtag_url = '/static/tool/main/hashtag-solid.svg'
const toolBarTRRef = ref(null)
const props = defineProps({
    title: String,
    intro: String,
    toolDetail: Object
})

const emit = defineEmits(['search-results', 'search-cleared', 'search-focused'])

const handleSearchResults = (searchData) => {
    emit('search-results', searchData)
}

const handleSearchCleared = () => {
    emit('search-cleared')
}

const handleSearchFocused = () => {
    emit('search-focused')
}

// Expose the performSearch method to parent components
const performSearch = async (query, page = 1) => {
    if (toolBarTRRef.value && toolBarTRRef.value.performSearch) {
        await toolBarTRRef.value.performSearch(query, page)
    }
}

const setPreventClearOnBlur = () => {
    if (toolBarTRRef.value && toolBarTRRef.value.setPreventClearOnBlur) {
        toolBarTRRef.value.setPreventClearOnBlur()
    }
}

defineExpose({
    performSearch,
    setPreventClearOnBlur
})

</script>

<style lang="scss" scoped>
.toolhead {
    box-shadow: 0 0 2px 0 rgba(0,0,0,0.5);
}

.hashsvg {
    filter: invert(100%) sepia(3%) saturate(7453%) hue-rotate(138deg) brightness(111%) contrast(104%);
}
</style>