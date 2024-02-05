<template>

    <div class="tooldetail bg-tooldetail-bg flex grow bg-orange-50 w-full">
        <!-- Component changes when currentTab changes -->
        <component :is="tabs['currentTab']"></component>
    </div>

</template>

<script setup>
import { ref, shallowRef } from 'vue'
import ToolTypical from './ToolTypical/ToolTypical.vue'
const tabs = shallowRef({
    'currentTab': ToolTypical,

})

</script>

<style lang="scss" scoped>

</style>