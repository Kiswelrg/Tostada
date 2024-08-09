<template>
    <svg ref="svg"
         xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 448 512">
        <path :stroke="stroke"
              :fill="stroke"
              d="M248 72c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 160L40 232c-13.3 0-24 10.7-24 24s10.7 24 24 24l160 0 0 160c0 13.3 10.7 24 24 24s24-10.7 24-24l0-160 160 0c13.3 0 24-10.7 24-24s-10.7-24-24-24l-160 0 0-160z" />
    </svg>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const stroke = ref(undefined)
const svg = ref(null)

onMounted(() => {
    // if (svg.value) {
    //     const computedStyle = window.getComputedStyle(svg.value)
    //     console.log('SVG color:', computedStyle.color)
    // }
})

watch(svg, (newValue) => {
    if (newValue) {
        const computedStyle = window.getComputedStyle(newValue)
        stroke.value = computedStyle.color
        // console.log('SVG color (from watcher):', computedStyle.color)
    }
}, { immediate: true })
</script>

<style scoped>
/* Add any scoped styles if necessary */
</style>