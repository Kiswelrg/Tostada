<template>
    <div class="h-16 w-full flex shadow-lg">
        <div class="wrapper text-[#000000] flex items-center my-1 ml-2">
            <div class="site-icon shrink-0 grow-0">
                <img src="@/assets/main/myserver.jpg" alt="" class="h-12 w-12 aspect-square rounded-full">
            </div>
            <div class="site-title mx-2 text-xl">
                <span>
                    Tostada
                </span>
            </div>
        </div>
        <div class="wrapper w-full flex items-center my-1 justify-end">
            <div class="flex items-center h-full mx-1 shrink-0 rounded-sm">
                <button
                    type="button"
                    class="button inline-block rounded bg-neutral-50 px-6 pb-2 pt-2.5 text-[11px] font-medium uppercase leading-normal text-neutral-800 shadow-[0_4px_9px_-4px_#cbcbcb] transition duration-150 ease-in-out hover:bg-neutral-100 hover:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] focus:bg-neutral-100 focus:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] focus:outline-none focus:ring-0 active:bg-neutral-200 active:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] dark:hover:shadow-[0_4px_9px_-4px_rgba(251,251,251,0.3)] dark:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] dark:focus:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] dark:active:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] bg-white text-[#000000]">
                    Login
                    </button>
            </div>
            <div class="flex items-center h-full mx-1 shrink-0 rounded-sm">
                <button
                    type="button"
                    class="button inline-block rounded bg-neutral-50 px-6 pb-2 pt-2.5 text-[11px] font-medium uppercase leading-normal text-neutral-800 shadow-[0_4px_9px_-4px_#cbcbcb] transition duration-150 ease-in-out hover:bg-neutral-100 hover:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] focus:bg-neutral-100 focus:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] focus:outline-none focus:ring-0 active:bg-neutral-200 active:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] dark:hover:shadow-[0_4px_9px_-4px_rgba(251,251,251,0.3)] dark:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] dark:focus:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] dark:active:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] bg-white text-[#000000]">
                    Signup
                    </button>
            </div>
            <!-- <div class="flex items-center w-16 h-full mx-1 shrink-0 rounded-sm">
                <button class="text-[12px] font-bold h-full w-16 mx-auto bg-[#616161] py-0">
                    注册
                </button>
            </div> -->
        </div>
    </div>

</template>

<script setup>

</script>

<style lang="scss" scoped>
.button {
    box-shadow: 0 1px 1px 1px #b0b0b0;
}
</style>