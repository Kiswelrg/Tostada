<template>

    <div class="args relative flex flex-col w-full h-fit bg-arg-base relative rounded-t-[4px] pt-1" save="bottom-[var(--m-inputking-height)] translate-x-[var(--m-inputking-l-idt)]">
        <div 
            @wheel.prevent="handleWheel"
            ref="arg"
            :class="{' mb-2 ' : !arg_OverflowX}"
            class="arg h-fit text-[1rem] text-left px-2 flex gap-2 mt-0 overflow-x-auto">
                <div v-for="_ in 3" :key="1" class="w-[150px] h-fit grow-0 shrink-0">
                    <label for="city" class="block text-[10px] font-medium leading-2 text-gray-900">City</label>
                    <div class="mt-0.5">
                        <textarea rows="4" type=" text" name="city" id="city" class="arg-input resize-none block w-full rounded-md border-0 px-1 py-1.5 text-[#eeeeee] text-[8px] shadow-sm placeholder:text-gray-800 sm:text-sm sm:leading-2 bg-[color:#585858]"></textarea>
                    </div>
                </div>
            
        </div>
        
    </div>
        

</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
const arg = ref(null);
const arg_OverflowX = ref(false);

onMounted(() => {
    const observer = new MutationObserver(checkOverflowX);
    
    if (arg.value) {
    observer.observe(arg.value, { childList: true, subtree: true });
    checkOverflowX();
    }
    
})

function handleWheel (e) {
  // Adjust scrollLeft property based on the wheel delta
  if (arg.value) {
    arg.value.scrollLeft += e.deltaY;
    }
}

const checkOverflowX = () => {
    if (arg.value)
        arg_OverflowX.value = arg.value.scrollWidth > arg.value.clientWidth;
};

watch(arg, () => {
    checkOverflowX();
});


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

.arg {
    &::-webkit-scrollbar {
        background-color: transparent;
        height: 8px;
        width: 100%;
    }
    &::-webkit-scrollbar-thumb {
        background-color: rgb(61, 61, 61);
        // border: 4px solid #2b2d31;
        border: 2px solid rgba(0,0,0,0);
        background-clip: padding-box;
        border-radius: 5px;
    }
    &::-webkit-scrollbar-button:start, &::-webkit-scrollbar-button:end {
        width: 3px;
    }
}
</style>