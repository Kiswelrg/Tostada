<template>
    <div class="TwoByTwoGrid grid grid-rows-2 grid-cols-2 gap-1 max-h-[350px]">
        <VisualMosaicItem :item="item" v-for="(item, idx) in props.items"></VisualMosaicItem>
    </div>
</template>

<script setup>
import VisualMosaicItem from '../Item/VisualMosaicItem.vue'
const props = defineProps([
    'items'
])
</script>

<style lang="scss" scoped>

</style>