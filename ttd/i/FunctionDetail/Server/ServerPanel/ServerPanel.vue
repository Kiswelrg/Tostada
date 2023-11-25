<template>
    <div class="serverpanel flex flex-col flex-auto bg-orange-100">
        <ServerHead></ServerHead>
        <ToolList></ToolList>
        <UserBar />
    </div>
</template>

<script setup>
import ServerHead from "./ServerHead/ServerHead.vue"
import ToolList from "./ToolList/ToolList.vue"
import UserBar from "@/../i/UserBar/UserBar.vue";
</script>

<style lang="scss" scoped>
.server {
    .serverpanel {
        background-color: #2b2d31;
        width: 240px;
    }
}
</style>