<template>
    <div class="serverpanel h-full w-[240px] bg-serverpanel-bg flex flex-col grow-0 shrink-0 bg-orange-100">
        <div class="wrapper h-[calc(100%-var(--m-userbar-height))] items-stretch justify-start flex-auto">
            <ServerHead></ServerHead>
            <ToolList @select-tool="selectTool"></ToolList>
        </div>
        <UserBar />
    </div>
</template>

<script setup>
import ServerHead from "./ServerHead/ServerHead.vue"
import ToolList from "./ToolList/ToolList.vue"
import UserBar from "@/i/Global/UserBar/UserBar.vue"
import { onMounted } from "vue"
const emit = defineEmits([
    'selectToolById'
])
function selectTool(id) {
    emit('selectToolById', id)
}


</script>

<style lang="scss" scoped>

</style>