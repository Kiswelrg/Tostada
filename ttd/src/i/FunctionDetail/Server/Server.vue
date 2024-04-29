<template>
    <div class="server flex flex-row grow overflow-hidden">
      <ServerPanel @select-tool-by-id="onSelectToolById"/>
      <ToolDetail :selected-tool="selectedTool"/>
    </div>
</template>

<script setup>
import ServerPanel from "./ServerPanel/ServerPanel.vue"
import ToolDetail from "./ToolDetail/ToolDetail.vue"
import { ref } from "vue";
const selectedTool = ref({});

function onSelectToolById(obj) {
  selectedTool.value = obj;
}

</script>

<style lang="scss" setup>
.server {

}
</style>