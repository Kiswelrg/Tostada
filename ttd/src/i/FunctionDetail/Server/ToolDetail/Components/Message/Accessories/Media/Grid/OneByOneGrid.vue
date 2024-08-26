<template>
    <div class="OneByOneGrid flex max-h-[280px] w-full">
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