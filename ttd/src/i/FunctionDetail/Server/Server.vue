<template>
    <div class="server flex flex-row grow overflow-hidden">
      <ServerPanel @select-tool-by-id="onSelectTool"/>
      <ToolDetail :selected-tool="selectedTool"/>
    </div>
</template>

<script setup>
import ServerPanel from "./ServerPanel/ServerPanel.vue"
import ToolDetail from "./ToolDetail/ToolDetail.vue"
import { ref } from "vue";
const selectedTool = ref({});

function onSelectTool(obj) {
  selectedTool.value = obj;
}

</script>

<style lang="scss">

</style>