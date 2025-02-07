<template>
    <a class="message-text anchor text-[color:var(--text-link)]" :href="msgURL" :style="{'display': [msgDisplay], 'font-size': [msgFSize]}" target="_blank"><span>{{ msgText }}</span></a>
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

const msgText = computed(() => {
    let res = ''
    if (!props.msgItem || !props.msgItem['text_display']) 
        res = props.msgItem['content'].slice(0,30) + (props.msgItem['content'].length > 30 ? '...' : '')
    else
        res = props.msgItem['text_display']
    return `${import.meta.env.VITE_BACKEND_URL}${res}`
})

const msgFSize = computed(() => {
    if (!props.msgItem || !('font-size' in props.msgItem)) return ''
    return props.msgItem['font-size']
})

const msgURL = computed(() => {
    if (!props.msgItem || !('content' in props.msgItem)) return '#'
    return `${import.meta.env.VITE_BACKEND_URL}${props.msgItem['content']}`
})

</script>

<style lang="scss" scoped>


</style>
