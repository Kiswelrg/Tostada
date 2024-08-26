<template>
    <div class="message-accessories grid empty:hidden h-fit indent-0 min-h-0 min-w-0 py-[0.125rem] relative">
        <VisualMediaContainer :media-items="visualMedias" v-if="hasImageObject"></VisualMediaContainer>
        <NonVisualMediaContainer :media-items="nonVisualMedias" v-if="hasNonImageObject"></NonVisualMediaContainer>
    </div>
</template>

<script setup>
import VisualMediaContainer from './Media/VisualMedia.vue'
import NonVisualMediaContainer from './Media/NonVisualMedia.vue'
import { computed } from 'vue'

const props = defineProps([
    'attachments'
])


const allowedImgExts = [
    'png',
    'jpg',
    'jpeg',
    'webp',
    'gif',
    'bmp',
]
const isFileImage = (obj) => {
    const extension = obj.name.split('.').pop().toLowerCase()
    return allowedImgExts.includes(extension)
}
const hasImageObject = computed(() => {
    if (props.attachments === undefined) return false
    return props.attachments.some(obj => {
        return isFileImage(obj)
    });
})
const hasNonImageObject = computed(() => {
    if (props.attachments === undefined) return false
    return props.attachments.some(obj => {
        return !isFileImage(obj)
    });
})
const visualMedias = computed(() => {
    if (props.attachments === undefined) return []
    return props.attachments.filter(obj => isFileImage(obj))
})
const nonVisualMedias = computed(() => {
    if (props.attachments === undefined) return []
    return props.attachments.filter(obj => !isFileImage(obj))
})



</script>

<style lang="scss" scoped>

</style>