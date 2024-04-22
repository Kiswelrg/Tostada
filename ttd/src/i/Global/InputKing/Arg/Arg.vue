<template>
    <div class="argument relative flex flex-col min-h-[calc(var(--m-onearg-h)+var(--m-args-rounded-offset))] h-fit w-full grow-0 shrink-0 bg-[#313338] translate-y-[var(--m-args-rounded-offset)] z-0">
        <ArgV :cur-method-detail="curMethodDetail" :cur-args="curArgs" @update-args="handleUpdateArgs"></ArgV>
        <div class="offset-holder h-[var(--m-args-rounded-offset)] w-full bg-arg-base"></div>
    </div>
</template>

<script setup>
import ArgV from './ArgType/ArgV.vue';
import ArgH from './ArgType/ArgH.vue';
const emits = defineEmits([
    'update-args'
])

const props = defineProps([
    'cur-method-detail',
    'cur-args'
])

const handleUpdateArgs = (v, key) => {
    emits('update-args', v, key)
}

</script>

<style lang="scss">
:root {
    --m-inputking-height: 53px;
    --m-inputking-l-idt: 24px;
    --m-onearg-h: 18px;
    --m-args-rounded-offset: 8px;
}
</style>

<style lang="scss" scoped>

</style>