<template>
    <div class="OneByTwoGrid flex flex-row gap-1 max-h-[280px]">
        <template v-if="props.items.length == 2">
            <OneByTwoItem :item="props.items[0]"></OneByTwoItem>
            <OneByTwoItem :item="props.items[1]"></OneByTwoItem>
        </template>
        <template v-else>
            <OneByTwoSoloItem :item="props.items[0]"></OneByTwoSoloItem>
            <OneByTwoDuoItem :items="props.items.slice(1)"></OneByTwoDuoItem>
        </template>
    </div>
</template>

<script setup>
import OneByTwoItem from './GridItem/OneByTwoItem.vue'
import OneByTwoSoloItem from './GridItem/OneByTwoSoloItem.vue'
import OneByTwoDuoItem from './GridItem/OneByTwoDuoItem.vue'


const props = defineProps([
    'items'
])
</script>

<style lang="scss" scoped>

</style>