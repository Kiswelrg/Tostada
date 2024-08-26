<template>
    <div class="visualMediaContainer w-full h-full max-w-[550px] rounded-[8px] overflow-hidden justify-self-start self-start">
        <div v-if="itemNum < 1">Error, No Attachment!</div>
        <OneByOneGrid v-if="itemNum == 1" :item="props.mediaItems[0]" :isAlone="true">
        </OneByOneGrid>

        <OneByTwoGrid v-else-if="itemNum <= 3" :items="props.mediaItems">
        </OneByTwoGrid>

        <TwoByTwoGrid v-else-if="itemNum <= 4" :items="props.mediaItems">
        </TwoByTwoGrid>

        <template v-else-if="itemNum <= 5">
            <OneByTwoGrid :items="props.mediaItems.slice(0,2)"></OneByTwoGrid>
            <ThreeByThreeGrid :items="props.mediaItems.slice(2)"></ThreeByThreeGrid>
        </template>

        <ThreeByThreeGrid v-else-if="itemNum <= 6" :items="props.mediaItems">
        </ThreeByThreeGrid>

        <template v-else-if="itemNum <= 7">
            <OneByOneGrid :item="props.mediaItems[0]" :isAlone="false"></OneByOneGrid>
            <ThreeByThreeGrid :items="props.mediaItems.slice(1)"></ThreeByThreeGrid>
        </template>

        <template v-else-if="itemNum <= 8">
            <OneByTwoGrid :items="props.mediaItems.slice(0,2)"></OneByTwoGrid>
            <ThreeByThreeGrid :items="props.mediaItems.slice(2)"></ThreeByThreeGrid>
        </template>

        <ThreeByThreeGrid v-else-if="itemNum <= 9" :items="props.mediaItems">
        </ThreeByThreeGrid>

        <template v-else-if="itemNum <= 10">
            <OneByOneGrid :item="props.mediaItems[0]" :isAlone="false"></OneByOneGrid>
            <ThreeByThreeGrid :items="props.mediaItems.slice(1)"></ThreeByThreeGrid>
        </template>

        <div v-else>
            Too Many Attachments!
        </div>
    </div>
</template>

<script setup>
import OneByTwoGrid from './Grid/OneByTwoGrid.vue'
import TwoByTwoGrid from './Grid/TwoByTwoGrid.vue'
import ThreeByThreeGrid from './Grid/ThreeByThreeGrid.vue'
import OneByOneGrid from './Grid/OneByOneGrid.vue'
import { computed } from 'vue'

const props = defineProps([
    'media-items'
])

const itemNum = computed(()=>{
    return props.mediaItems.length
})


</script>

<style lang="scss" scoped>

</style>