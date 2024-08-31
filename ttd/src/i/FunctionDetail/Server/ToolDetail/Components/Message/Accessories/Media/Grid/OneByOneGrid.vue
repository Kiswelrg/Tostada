<template>
    <div class="OneByOneGrid " :class="{'max-h-[280px]': !props.isAlone, 'max-h-[350px]': props.isAlone, 'w-full': !props.isAlone, 'w-fit': props.isAlone, 'max-w-full': props.isAlone, 'inline-block': props.isAlone, 'flex': props.isAlone === undefined || !props.isAlone, 'rounded-[8px]': props.isAlone, 'overflow-hidden': props.isAlone}">
        <VisualMosaicItem :item="props.item" :isAlone="props.isAlone">
            
        </VisualMosaicItem>
    </div>
</template>

<script setup>
import VisualMosaicItem from '../Item/VisualMosaicItem.vue'
const props = defineProps([
    'item',
    'isAlone'
])
</script>

<style lang="scss" scoped>

</style>