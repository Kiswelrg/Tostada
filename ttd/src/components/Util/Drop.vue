<template>
    <div class="relative inline-block text-left">
        <div class="h-full flex">
            <button type="button"
                    class="inline-flex w-full justify-center items-center gap-x-1.5 rounded-md bg-dark-interactive-normal px-3 py-2 text-[8px] font-semibold text-inputking-bg shadow-sm hover:bg-dark-interactive-hover focus:outline-none hover:border-white"
                    @click="isDropMenuOpen = !isDropMenuOpen"
                    ref="triggerRef"
                    id="menu-button"
                    aria-expanded="true"
                    aria-haspopup="true">
                Bots
                <svg class="-mr-1 h-3 w-3 text-gray-400"
                     viewBox="0 0 20 20"
                     fill="currentColor"
                     aria-hidden="true">
                    <path fill-rule="evenodd"
                          d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
                          clip-rule="evenodd" />
                </svg>
            </button>
            <div class="h-full w-4 absolute right-[-4px] top-0 content-top text-black z-10 text-[8px]">({{ methodsNum }})</div>
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
             class="absolute right-0 z-10 m-0 py-0.5 origin-bottom-right rounded-md bg-dark-dropmenu-thumb shadow-lg focus:outline-none"
             :class="{hidden: !isDropMenuOpen}"
             v-click-outside="[closeMenu, triggerRef]"
             role="menu"
             aria-orientation="vertical"
             aria-labelledby="menu-button"
             tabindex="-1">
            <div
                v-for="group in methods.toReversed()"
                :key="group.index"
                class="py-[1.5px]"
                role="none">
                <div
                    v-for="method in group.methods.toReversed()"
                    :key="method.cid"
                    :class="{'pl-2': !props.hasIcon, 'pl-2': props.hasIcon, 'bg-white': isMethodActive(method.cid), 'hover:bg-dark-interactive-normal': !isMethodActive(method.cid)}"
                    class="menu-item flex items-center mx-1 hover:text-black rounded-sm">
                    <div :class="{'hidden': !props['hasIcon']}" class="item-icon px-0">
                        <div class="flex">
                            <font-awesome-icon :icon="['fas', 'ellipsis-h']" class="block h-2 w-2 object-contain" :style="{color : colors.darkFilterNormal}"/>
                        </div>
                    </div>
                    <a href="#"
                        :class="{'pl-2': !props.hasIcon, 'pl-0.5': props.hasIcon, 'text-black': isMethodActive(method.cid),'text-dark-interactive-normal': !isMethodActive(method.cid)}"
                        @click="chooseMethod(method)"
                        class="inline-block break-words max-w-32 min-w-[57px] pr-4 py-0.5 text-[10px] hover:text-black"
                        role="menuitem"
                        tabindex="-1"
                        id="menu-item-6">{{ method.display_name }}</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import colors from 'tailwindcss/colors'

const emit = defineEmits([
    'onChooseMethod',
])

const triggerRef = ref(null)

const props = defineProps([
    'down',
    'height',
    'menu-gap',
    'has-icon',
    'methods-list',
    'cur-method'
])
const currentMethodCid = ref(0)
const isUsingDefault = ref(false)
const isDropMenuOpen = ref(false)

const isMethodActive = (g_cid) => {
    return g_cid == currentMethodCid.value
}

const methodsNum = computed(() => {
  if (props.methodsList) {
    if (!props.methodsList.groups) return 0;
    let res = 0;
    for (const g of props.methodsList.groups) {
        res += g.methods ? g.methods.length : 0;
    }
    return res;
  }
  return 0;
});

const chooseMethod = (m) => {
    currentMethodCid.value = m.cid
    emit('onChooseMethod', m)
}

const methods = computed(() => {
    let res = [{
        index: 1,
        methods: [{
            cid: 0,
            display_name: '聊天',
            input: [],
            output: []
        }]
    }]
    if (props.methodsList) {
        for (const i in props.methodsList['groups']) {
            const group = props.methodsList['groups'][i]
            if (!group) continue
            let g = {
                index: group.index,
                methods: []
            }
            for (const m of group.methods) {
                g.methods.push({
                    cid: m.cid,
                    display_name: m.display_name,
                    description: m.description,
                    input: m.input,
                    output: m.output
                })
            }
            res.push(g)
        }
        // return res.concat(props.methodsList['groups'])
    }
        
    return res
})

watch(methods, (newl) => {
    currentMethodCid.value = 0
    if (newl.length && props.curMethod === -1) isUsingDefault.value = true
    else isUsingDefault.value = false
})


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