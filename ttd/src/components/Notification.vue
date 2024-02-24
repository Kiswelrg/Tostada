<template>
    <div>
        {{ notification }}
    </div>
</template>

<script setup>
const p = defineProps(['notification'])
const notification = p.notification

</script>

<style lang="scss" scoped>

</style>

