<template>
    <div class="menu relative flex min-w-[188px] max-w-[320px] h-auto cursor-default max-h-[calc(100vh-32px)] rounded-[4px] bg-[var(--background-floating)] shadow-[var(--shadow-high)] z-10">
        <div class="relative text-white scroller px-2 py-1.5 flex-auto">
            <div class="group pt-1 pr-0 pb-1.5 pl-0.5 h-8">1</div>
            <div class="group">
                <item class="flex min-h-8 items-center px-2 py-1.5 justify-between mx-0 my-0.5 rounded-[2px] text-[14px] font-medium leading-[18px] cursor-pointer outline-0">Edit Message</item>
                <item class="flex min-h-8 items-center px-2 py-1.5 justify-between mx-0 my-0.5 rounded-[2px] text-[14px] font-medium leading-[18px] cursor-pointer outline-0">Copy Text</item>
                <item class="flex min-h-8 items-center px-2 py-1.5 justify-between mx-0 my-0.5 rounded-[2px] text-[14px] font-medium leading-[18px] cursor-pointer outline-0">Copy Message Link</item>
                <item class="flex min-h-8 items-center px-2 py-1.5 justify-between mx-0 my-0.5 rounded-[2px] text-[14px] font-medium leading-[18px] cursor-pointer outline-0">Delete Message</item>
            </div>
        </div>
    </div>
</template>

<script setup>

</script>

<style lang="scss">
:root {
    
}
</style>

<style lang="scss" scoped>

</style>