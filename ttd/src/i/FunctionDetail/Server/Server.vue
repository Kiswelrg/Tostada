<template>
    <div class="server flex flex-row grow overflow-hidden">
      <ServerPanel @select-tool-by-id="onSelectToolById"/>
      <ToolDetail :selected-tool-id="selectedToolId"/>
    </div>
</template>

<script setup>
import ServerPanel from "./ServerPanel/ServerPanel.vue"
import ToolDetail from "./ToolDetail/ToolDetail.vue"
import { ref } from "vue";
const selectedToolId = ref(-1);

function onSelectToolById(id) {
  selectedToolId.value = id;
}

</script>

<style lang="scss" setup>
.server {

}
</style>