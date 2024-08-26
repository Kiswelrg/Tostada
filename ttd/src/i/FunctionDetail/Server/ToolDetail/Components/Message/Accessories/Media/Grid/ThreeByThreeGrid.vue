<template>
    <div class="ThreeByThreeGrid mt-1 grid grid-cols-3 gap-1">
        <VisualMosaicItem v-for="(item, idx) in props.items" :item="item"></VisualMosaicItem>
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