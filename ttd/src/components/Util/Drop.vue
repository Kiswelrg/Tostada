<template>
    <div class="relative inline-block text-left">
        <div>
            <button type="button"
                    class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-dark-interactive-normal px-3 py-2 text-[8px] font-semibold text-inputking-bg shadow-sm hover:bg-dark-interactive-hover focus:outline-none hover:border-white"
                    @click="isDropMenuOpen = !isDropMenuOpen"
                    ref="triggerRef"
                    id="menu-button"
                    aria-expanded="true"
                    aria-haspopup="true">
                Options
                <svg class="-mr-1 h-3 w-3 text-gray-400"
                     viewBox="0 0 20 20"
                     fill="currentColor"
                     aria-hidden="true">
                    <path fill-rule="evenodd"
                          d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
                          clip-rule="evenodd" />
                </svg>
            </button>
        </div>

        <!--
      Dropdown menu, show/hide based on menu state.
  
      Entering: "transition ease-out duration-100"
        From: "transform opacity-0 scale-95"
        To: "transform opacity-100 scale-100"
      Leaving: "transition ease-in duration-75"
        From: "transform opacity-100 scale-100"
        To: "transform opacity-0 scale-95"
    -->
        <div :style="menuPosition"
             class="absolute right-0 z-10 m-0 origin-bottom-right rounded-md bg-dark-dropmenu-thumb shadow-lg focus:outline-none"
             :class="{hidden: !isDropMenuOpen}"
             v-click-outside="[closeMenu, triggerRef]"
             role="menu"
             aria-orientation="vertical"
             aria-labelledby="menu-button"
             tabindex="-1">
            <div
                v-for="group in methods"
                class="py-1"
                role="none">
                <div
                    v-for="method in group.methods"
                    :class="{'pl-2': !props.hasIcon, 'pl-2': props.hasIcon}"
                    class="menu-item flex items-center mx-1 hover:bg-dark-interactive-normal hover:text-black rounded-sm">
                    <div :class="{'hidden': !props['hasIcon']}" class="item-icon px-0">
                        <div class="flex">
                            <font-awesome-icon :icon="['fas', 'ellipsis-h']" class="block h-2 w-2 object-contain" :style="{color : colors.darkFilterNormal}"/>
                        </div>
                    </div>
                    <a href="#"
                        :class="{'pl-2': !props.hasIcon, 'pl-0.5': props.hasIcon}"
                       class="inline-block break-words max-w-32 min-w-[57px] pr-4 py-0.5 text-[10px] text-dark-interactive-normal hover:text-black"
                       role="menuitem"
                       tabindex="-1"
                       id="menu-item-6">{{ method.display_name }}</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import colors from 'tailwindcss/colors'

const triggerRef = ref(null)

const props = defineProps([
    'down',
    'height',
    'menu-gap',
    'has-icon',
    'methods-list',
])

const methods = computed(() => {
    if (props.methodsList)
        return props.methodsList['groups']
    return []
})

const isDropMenuOpen = ref(true);

const closeMenu = () => {
    if (!isDropMenuOpen.value) return;
    isDropMenuOpen.value = false;
}

const menuPosition = computed(() => {
    return props.down
        ? { top: `${props.height + props.menuGap}px` }
        : { bottom: `${props.height + props.menuGap}px` }
})


</script>

<style scoped lang="scss">

</style>