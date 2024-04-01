<template>
    <div class="inputking flex flex-col px-2 h-[var(--m-inputking-height)] w-full grow-0 shrink-0 bg-[#313338]">
        <div class="wrapper flex justify-between mb-1 bg-[#383a40] w-full h-full rounded-lg">
            <div class="left-buttons h-full flex items-center ml-2">
                <div>
                    <div class="h-8 w-8 bg-[#2f2f2f] rounded-lg"></div>
                </div>
            </div>
            <div class="main-input items-center w-full h-full flex mx-2">

                <div class="flex rounded-md shadow-sm w-full h-full">
                    <input type="text" placeholder="Message here" class="w-full text-md my-2 bg-[#383a40] outline-none font-light">
                </div>

            </div>
            <div class="main-input items-center w-16 flex mx-2">

                <div class="flex shadow-sm w-16 h-8">
                    <input type="submit" class="border-[1px] w-full h-8 rounded-md text-[12px] my-auto bg-[#2f3135] hover:bg-[#4f5258] outline-none font-light">
                </div>

            </div>
            <div class="hidden flex right-buttons h-full items-center mr-2">
                <div>
                    <div class="mx-1 h-8 w-8 bg-[#2f2f2f] rounded-lg"></div>
                </div>
                <div>
                    <div class="mx-1 h-8 w-8 bg-[#2f2f2f] rounded-lg"></div>
                </div>
                <div>
                    <div class="mx-1 h-8 w-8 bg-[#2f2f2f] rounded-lg"></div>
                </div>
            </div>
        </div>
        <div class="h-0.5 translate-y-[1px] w-full bg-white rounded-lg"></div>
        <div class="args max-w-[calc(100%-64px)] min-w-8 h-6 bg-text-muted absolute bottom-[var(--m-inputking-height)] translate-x-[var(--m-inputking-l-idt)] rounded-t-[4px]">
            1
        </div>
    </div>
</template>

<script setup>

</script>


<style lang="scss">
:root {
    --m-inputking-height: 53px;
    --m-inputking-l-idt: 24px;
}
</style>
<style lang="scss" scoped></style>