<template>
    <div class="absolute h-screen w-screen">
        <Popups v-if="showPopups"></Popups>
    </div>
</template>

<script setup>
import Popups from './Popup/Popups.vue'
import { ref } from 'vue'

const showPopups = ref(true)

</script>

<style lang="scss" scoped>

</style>