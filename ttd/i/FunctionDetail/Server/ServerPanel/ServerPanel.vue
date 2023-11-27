<template>
    <div class="serverpanel w-[240px] bg-serverpanel-bg flex flex-col flex-grow-0 flex-shrink-0 bg-orange-100">
        <div class="wrapper h-full items-stretch justify-start flex-auto">
            <ServerHead></ServerHead>
            <ToolList></ToolList>
        </div>
        <UserBar />
    </div>
</template>

<script setup>
import ServerHead from "./ServerHead/ServerHead.vue"
import ToolList from "./ToolList/ToolList.vue"
import UserBar from "@/../i/Global/UserBar/UserBar.vue"

</script>

<style lang="scss" scoped>

</style>