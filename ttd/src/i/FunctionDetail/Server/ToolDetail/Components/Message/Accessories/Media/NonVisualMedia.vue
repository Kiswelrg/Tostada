<template>
    <div class="nonVisualMediaContainer mt-2 max-w-full flex flex-col justify-self-start self-start">
        <NonVisualMediaItem v-for="(item, idx) in props.mediaItems" :key="item.cid || idx" :item="item" @attachment-deleted="handleAttachmentDeleted"></NonVisualMediaItem>
    </div>
</template>

<script setup>
import NonVisualMediaItem from './Item/NonVisualMosaicItem.vue'

const props = defineProps([
    'media-items'
])

const emit = defineEmits(['attachment-deleted'])

const handleAttachmentDeleted = (attachmentCID) => {
    emit('attachment-deleted', attachmentCID)
}

</script>

<style lang="scss" scoped>

</style>