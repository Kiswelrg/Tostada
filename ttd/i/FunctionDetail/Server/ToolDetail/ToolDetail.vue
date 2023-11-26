<template>

    <div class="tooldetail flex grow basis-full bg-orange-50 w-full">
        <!-- Component changes when currentTab changes -->
        <component :is="tabs['currentTab']"></component>
    </div>

</template>

<script setup>
import { ref } from 'vue'
import ToolTypical from './ToolTypical/ToolTypical.vue'
const tabs = ref({
    'currentTab': ToolTypical,

})

</script>

<style lang="scss" scoped>
.server {
    .tooldetail {
        background-color: #313338;
    }
}
</style>