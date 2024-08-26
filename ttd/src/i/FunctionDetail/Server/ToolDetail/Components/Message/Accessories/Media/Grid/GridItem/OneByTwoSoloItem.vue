<template>
    <div class="OneByTwoSoloItem grow-[2] shrink basis-0">
        <VisualMosaicItem :item="props.item"></VisualMosaicItem>
    </div>
</template>

<script setup>
import VisualMosaicItem from '../../Item/VisualMosaicItem.vue'
const props = defineProps([
    'item'
])
</script>

<style lang="scss" scoped>

</style>