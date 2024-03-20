<template>
    <div class="server flex flex-row w-full">
      <ServerPanel @select-tool-by-id="onSelectToolById"/>
      <ToolDetail />
    </div>
</template>

<script setup>
import ServerPanel from "./ServerPanel/ServerPanel.vue"
import ToolDetail from "./ToolDetail/ToolDetail.vue"
import { ref } from "vue";
import { provide } from 'vue';
const selectedToolId = ref(-1);
provide('selected-tool-id', selectedToolId);

function onSelectToolById(id) {
  selectedToolId.value = id;
}

</script>

<style lang="scss" setup>
.server {

}
</style>