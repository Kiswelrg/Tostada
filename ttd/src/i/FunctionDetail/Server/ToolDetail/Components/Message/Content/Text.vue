<template>
    <span class="message-text normal" :style="{'display': [msgDisplay], 'font-size': [msgFSize]}">{{ props.msgItem.content}}</span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps([
    'msg-item'
])

const msgDisplay = computed(() => {
    if (!props.msgItem || !props.msgItem['display']) return ''
    return props.msgItem['display']
})

const msgFSize = computed(() => {
    if (!props.msgItem || !('font-size' in props.msgItem)) return ''
    return props.msgItem['font-size']
})

</script>

<style lang="scss" scoped>


</style>
