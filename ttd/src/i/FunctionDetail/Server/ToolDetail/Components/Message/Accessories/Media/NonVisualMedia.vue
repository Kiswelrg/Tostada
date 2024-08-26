<template>
    <div class="nonVisualMediaContainer mt-2 max-w-full flex flex-col justify-self-start self-start">
        <NonVisualMediaItem v-for="(item, idx) in props.mediaItems" :item="item"></NonVisualMediaItem>
    </div>
</template>

<script setup>
import NonVisualMediaItem from './Item/NonVisualMosaicItem.vue'

const props = defineProps([
    'media-items'
])

</script>

<style lang="scss" scoped>

</style>