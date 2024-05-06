<template>

    <div class="tooldetail bg-tooldetail-bg flex grow bg-orange-50 min-w-[300px]">
        <!-- Component changes when currentTab changes -->
        <component :is="tabs[currentTab]" :tool-detail="tool_detail" :introToMsg="introToMsg"></component>
    </div>

</template>

<script setup>
import { computed, ref, shallowRef } from 'vue'
import { watch } from 'vue';
import ToolTypical from './Tools/ToolTypical/ToolTypical.vue'
import { jsonWithBigInt } from '@/util/parse'
const props = defineProps([
    'selectedTool'
])

const currentTab = ref('ToolTypical')

const tool_detail = ref()

const tabs = shallowRef({
    'ToolTypical': ToolTypical,
})

const selectedToolId = computed(() => {
  return props.selectedTool.cid
})

const selectedToolSubclass = computed(() => {
  return props.selectedTool.sub_class
})


async function fetchToolDetail() {
  const response = await fetch(
    `/api/i/tool/${selectedToolSubclass.value}/${selectedToolId.value}/`,
    {
      method: "GET",
    }
  )
  
  if (response.ok) {
    const t = await response.text()
    const r = jsonWithBigInt(t)
    if (r.r) {
      tool_detail.value = r.tool
      console.log(`Tool (fetch status: ${r.r}): `, r.tool)
    } else {
      console.log(r, typeof(r))
    }
  } else {
    console.log(response.status)
  }
}

const watch_tool = watch(
  () => selectedToolId.value,
  async (newValue, old) => {
    if ( typeof newValue === 'bigint' ) {
      await fetchToolDetail()
    }
  }
)

const introToMsg = (intro) => {
  // intro = intro.filter(obj => !obj.hasOwnProperty('type'))
  return intro?.map(element => ({
    content: element.content,
    title: 'Tool Bot', // Replace 'someValue' with the value you want for the 'bot' attribute
    time: new Date().toISOString(), // Get the current time in ISO format
    avatar: '/api/i/default-bot-avatar/'
  }));

}

</script>

<style lang="scss" scoped>

</style>