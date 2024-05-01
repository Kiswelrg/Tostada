<template>
    <a class="message-text anchor" :href="msgURL" :style="{'display': [msgDisplay], 'font-size': [msgFSize]}"><span>{{ props.msgItem?.display_name }}</span></a>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps([
    "msg-item"
])

const msgDisplay = computed(() => {
    if (!props.msgItem || !props.msgItem['display']) return ''
    return props.msgItem['display']
})

const msgFSize = computed(() => {
    if (!props.msgItem || !('font-size' in props.msgItem)) return ''
    return props.msgItem['font-size']
})

const msgURL = computed(() => {
    if (!props.msgItem || !('url' in props.msgItem)) return ''
    return props.msgItem['url']
})

</script>

<style lang="scss" scoped>


</style>
