<template>
    <span class="message-text normal">{{ props.msgItem.content }}</span>
</template>

<script setup>
const props = defineProps([
    'msg-item'
])

</script>

<style lang="scss" scoped>


</style>
