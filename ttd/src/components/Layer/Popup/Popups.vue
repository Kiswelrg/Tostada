<template>
    <div class="popups absolute overflow-y-auto pointer-events-auto">
        <MsgOption v-if="popupType == 'MsgMenu'" class="" :cid="cid" @close-msg-menu="closeMsgMenu"></MsgOption>
    </div>
</template>

<script setup>
import MsgOption from './Menu/MsgOption.vue'

const emit = defineEmits([
    'onCloseMsgMenu'
])

const props = defineProps([
    'popup-type',
    'cid',
])

const closeMsgMenu = () => {
    emit('onCloseMsgMenu')
}

</script>

<style lang="scss" scoped>

</style>