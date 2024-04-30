<template>
    <span
            class="timestamp text-xs leading-[1.375rem] text-text-muted align-baseline inline-block h-6 cursor-default pointer-events-none font-light">
        <span class="edited text-625 select-none mx-1">({{ props.isEdited.text }})</span>
    </span>
</template>

<script setup>
const props = defineProps([
    'isEdited'
])

</script>

<style lang="scss" scoped>


</style>