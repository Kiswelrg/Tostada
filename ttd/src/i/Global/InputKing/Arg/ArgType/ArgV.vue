<template>

    <div class="args relative flex flex-col w-full h-fit bg-text-muted relative rounded-t-[4px] pt-1" save="bottom-[var(--m-inputking-height)] translate-x-[var(--m-inputking-l-idt)]">
        <div class="arg h-fit text-[1rem] text-left px-2 flex mt-0 overflow-x-auto">
                <div v-for="_ in 10" :key="1" class="w-[100px] h-fit">
                    <label for="city" class="block text-[10px] font-medium leading-2 text-gray-900">City</label>
                    <div class="mt-0.5">
                        <textarea rows="2" type=" text" name="city" id="city" class="arg-input resize-none block w-full rounded-md border-0 p-1 text-[#000000] text-[8px] shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-800 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-4"></textarea>
                    </div>
                </div>
            
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
.arg-input {
    &::-webkit-scrollbar {
        background-color: transparent;
        width: 10px;
        height: 100%;
    }
    &::-webkit-scrollbar-thumb {
        background-color: rgb(27, 27, 27);
        // border: 4px solid #2b2d31;
        border: 2px solid rgba(0,0,0,0);
        background-clip: padding-box;
        border-radius: 5px;
    }
    
}
</style>