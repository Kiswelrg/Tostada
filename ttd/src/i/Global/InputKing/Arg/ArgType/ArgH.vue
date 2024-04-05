<template>

    <div class="args flex flex-col w-full h-fit bg-text-muted relative rounded-t-[4px] pt-1" save="bottom-[var(--m-inputking-height)] translate-x-[var(--m-inputking-l-idt)]">
        <div v-for="_ in 4" class="arg h-5 text-[1rem] text-left px-2 flex">
            <div class="arg-name">argn</div>
            <input class="arg-input text-black" type="text"/>
        </div>
        
    </div>
        

</template>

<script setup>


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