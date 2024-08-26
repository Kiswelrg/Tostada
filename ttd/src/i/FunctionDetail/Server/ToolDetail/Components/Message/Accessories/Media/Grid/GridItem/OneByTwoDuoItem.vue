<template>
    <div class="OneByTwoDuoItem flex-1">
        <TwoByOneGrid :items="props.items"></TwoByOneGrid>
    </div>
</template>

<script setup>
import TwoByOneGrid from '../TwoByOneGrid.vue'

const props = defineProps([
    'items'
])
</script>

<style lang="scss" scoped>

</style>