<template>
    <div class="OneByTwoItem flex-1 min-w-0">
        <VisualMosaicItem :item="props.item">
            
        </VisualMosaicItem>
    </div>
</template>

<script setup>
import VisualMosaicItem from '../../Item/VisualMosaicItem.vue';
const props = defineProps([
    'item'
])

</script>

<style lang="scss" scoped>

</style>