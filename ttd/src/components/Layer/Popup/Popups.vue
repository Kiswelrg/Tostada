<template>
    <div class="popups absolute overflow-y-auto">
        <MsgOption v-if="popupType == 'MsgMenu'" class=""></MsgOption>
    </div>
</template>

<script setup>
import MsgOption from './Menu/MsgOption.vue'

const props = defineProps({
    popupType: String
})

</script>

<style lang="scss" scoped>

</style>