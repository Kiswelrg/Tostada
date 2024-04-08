<template>
<div class="flex z-[2] h-[var(--m-userbar-height)] grow-0 shrink-0 mb-px w-full pr-2 pl-[6px] bg-userbar-bg items-center">

    <div class="flex min-w-[120px] h-[42px] mr-2 pl-0.5 bg-userbar-hoverbg rounded-md items-center">
        <div class="h-8 w-8 shrink-0 rounded-full bg-hui-800 cursor-pointer"></div>
        <div class="h-[42px] grow mr-1 cursor-pointer py-1 pl-2 min-w-0 text-left">
            
            <div class="username-text whitespace-nowrap text-ellipsis overflow-hidden">
                <div>
                    kiswelrg
                </div>
            </div>
            <div class="status-text whitespace-nowrap text-ellipsis overflow-hidden">
                <div>
                    Online
                </div>
            </div>
            
        </div>
    </div>
    <div class="buttonlist flex flex-initial nowrap justify-start items-stretch">
        <div class="h-8 w-8 flex justify-center items-center rounded-md hover:bg-userbar-hoverbg"></div>
        <div class="h-8 w-8 flex justify-center items-center rounded-md hover:bg-userbar-hoverbg"></div>
        <div class="h-8 w-8 flex justify-center items-center rounded-md hover:bg-userbar-hoverbg"></div>
    </div>
    <div class="bg-red-400 h-5 w-5 absolute bottom-0"></div>
</div>
</template>

<script setup>

</script>


<style lang="scss">
:root {
    --m-userbar-height: 53px;
}
</style>

<style lang="scss" scoped>

.username-text {
    font-size: 14px;
    line-height: 18px;
    color: #f2f3f5;
}

.status-text {
    font-size: 12px;
    line-height: 16px;
    color: #b5bac1;
}
</style>