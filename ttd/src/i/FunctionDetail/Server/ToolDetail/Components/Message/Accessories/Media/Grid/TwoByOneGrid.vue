<template>
    <div class="TwoByOneGrid flex flex-col h-full gap-1">
        <TwoByOneItem :item="props.items[0]"></TwoByOneItem>
        <TwoByOneItem :item="props.items[1]"></TwoByOneItem>
    </div>
</template>

<script setup>
import TwoByOneItem from './GridItem/TwoByOneItem.vue'
const props = defineProps([
    'items'
])

</script>

<style lang="scss" scoped>

</style>