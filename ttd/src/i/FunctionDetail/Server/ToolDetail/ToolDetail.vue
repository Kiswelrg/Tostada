<template>

    <div class="tooldetail bg-tooldetail-bg flex grow bg-orange-50 w-full">
        <!-- Component changes when currentTab changes -->
        <component :is="tabs[currentTab]" :selected-tool-id="props.selectedToolId"></component>
    </div>

</template>

<script setup>
import { ref, shallowRef } from 'vue'
import { watch } from 'vue';
import ToolTypical from './Tools/ToolTypical/ToolTypical.vue'
const props = defineProps([
    'selectedToolId'
])

const currentTab = ref('ToolTypical')

const tabs = shallowRef({
    'ToolTypical': ToolTypical,
})

async function fetchToolDetail() {
  const response = await fetch(
    `/api/i/tool/${props.selectedToolId}/`,
    {
      method: "GET",
    }
  );
  
  if (response.ok) {
    const r = await response.json();
    console.log(`Tool ${props.selectedToolId} ( fetch status: ${r.r}): `, r.tool);
  } else {
    console.log(response.status);
  }
}

const watch_tool = watch(
  () => props.selectedToolId,
  async (newValue, old) => {
    console.log(newValue)
    if ( typeof newValue === 'number' ) {
      await fetchToolDetail()
    }
  }
)


</script>

<style lang="scss" scoped>

</style>