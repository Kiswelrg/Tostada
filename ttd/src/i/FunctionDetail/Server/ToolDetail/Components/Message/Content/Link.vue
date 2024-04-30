<template>
    <a class="message-text anchor"><span>{{ props.msgItem?.display_name }}</span></a>
</template>

<script setup>
const props = defineProps([
    "msg-item"
])


</script>

<style lang="scss" scoped>


</style>
