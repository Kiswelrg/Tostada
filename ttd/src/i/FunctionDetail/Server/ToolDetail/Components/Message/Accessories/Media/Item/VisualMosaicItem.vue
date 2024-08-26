<template>
    <div class="VisualMosaicItem group/visualmosaicitem overflow-hidden relative max-h-[inherit] rounded-sm w-full items-center justify-self-auto flex flex-row flex-nowrap max-w-full h-full">
        <div class="imageContent w-full h-full flex-auto flex flex-col flex-nowrap">
            <div class="imageContainer flex flex-row flex-nowrap flex-auto w-full h-full">
                <div class="imageWrapper block max-h-[inherit] m-auto h-full w-full" :class="{'aspect-square': props.imageSquare !== undefined && props.imageSquare}"
                :style="SoloWH">
                    <a :href="'/api' + props.item.url" target="_blank" class="originalLink absolute top-0 right-0 bottom-0 left-0 z-[1] text-[var(--text-link)] no-underline cursor-pointer"></a>
                    <div class="clickableWrapper w-full h-full">
                        <div class="loadingOverlay w-full h-full" :style="SoloRatio">
                            <img :src="'/api' + props.item.url" alt="" class="lazyImage block object-cover min-w-full min-h-full max-w-full -indent-[9999px]">
                        </div>
                    </div>

                </div>
                <div class="hoverButtonGroup flex opacity-0 z-[2] absolute rounded-[5px] top-1 right-1 bg-[color:var(--background-primary)] overflow-hidden group-hover/visualmosaicitem:opacity-100">
                    <div class="hoverButtonRemove flex p-[8px] text-[color:var(--interactive-normal)] cursor-normal hover:bg-[var(--menu-item-danger-active-bg)] hover:text-[var(--white)]">
                        <font-awesome-icon
                        :icon="['fas', 'trash']"
                        class="block h-4 w-4 object-contain"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { computed } from "vue"

const props = defineProps([
    'item',
    'isAlone',
    'image-square',
])

const SoloRatio = computed(() => {
    return `aspect-ratio:${props.item.dimensions[0]/props.item.dimensions[1]}/1;`
})

const SoloWH = computed(() => {
    if (props.isAlone === undefined || props.isAlone === false) return ''
    const w = props.item.dimensions[0];
    const h = props.item.dimensions[1];
    if (w <= 350 && h <= 350) return `width:${w}px;height:100%;`
    const default_ratio = 1;
    const cur_ratio = w / h;
    if (cur_ratio > default_ratio) {
        return `height:${350*h/w};width:350px;`
    } else {
        return `height:350px;width:${350*w/h};`
    }
})
</script>

<style lang="scss" scoped>

</style>