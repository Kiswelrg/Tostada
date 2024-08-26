<template>
    <div class="TwoByOneItem flex-1 min-h-0">
        <VisualMosaicItem :item="item"></VisualMosaicItem>
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