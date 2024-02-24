<template>
    <div class="serverpanel h-full w-[240px] bg-serverpanel-bg flex flex-col grow-0 shrink-0 bg-orange-100">
        <div class="wrapper h-[calc(100%-53px)] items-stretch justify-start flex-auto">
            <PanelHead></PanelHead>
            <PanelBody></PanelBody>
        </div>
        <UserBar />
    </div>
</template>

<script setup>
import PanelBody from "./PanelBody/PanelBody.vue";
import PanelHead from "./PanelHead/PanelHead.vue";
import UserBar from "@/i/Global/UserBar/UserBar.vue"

</script>

<style lang="scss" setup>

</style>