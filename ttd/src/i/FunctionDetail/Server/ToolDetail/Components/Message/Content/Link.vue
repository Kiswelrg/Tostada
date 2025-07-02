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
    if (!props.msgItem) return ''
    
    let res = ''
    if (!props.msgItem['text_display'] && props.msgItem['url']) {
        res = props.msgItem['url'].slice(0,30) + (props.msgItem['url'].length > 30 ? '...' : '')
    } else if (props.msgItem['text_display']) {
        res = props.msgItem['text_display']
    } else if (props.msgItem['content']) {
        // Fallback to content if url/text_display not available
        res = props.msgItem['content']
    }
    return res.startsWith('http') ? res : `${import.meta.env.VITE_BACKEND_URL}${res}`
})

const msgFSize = computed(() => {
    if (!props.msgItem || !('font-size' in props.msgItem)) return ''
    return props.msgItem['font-size']
})

const msgURL = computed(() => {
    if (!props.msgItem) return '#'
    
    const url = props.msgItem['url'] || props.msgItem['content'] || '#'
    return url.startsWith('http') ? url : `${import.meta.env.VITE_BACKEND_URL}${url}`
})

</script>

<style lang="scss" scoped>


</style>
