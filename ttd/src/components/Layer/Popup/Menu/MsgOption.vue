<template>
    <div class="menu relative flex min-w-[188px] max-w-[320px] h-auto cursor-default max-h-[calc(100vh-32px)] rounded-[4px] bg-[var(--background-floating)] shadow-[var(--shadow-high)] z-10">
        <div class="relative text-white scroller px-2 py-1.5 flex-auto">
            <div class="group grid pt-1 pr-[1px] pb-1.5 pl-[1px] h-auto grid-cols-4 grid-rows-[1fr] items-center justify-items-center outline-0">
                <div v-for="(react, i) in recent_reactions" :key="i" class="customItem text-[var(--interactive-normal)] border-[var(--interactive-normal)] text-[14px] font-medium leading-[18px]">
                    <div class="button flex items-center justify-center w-8 h-8 p-1 cursor-pointer rounded-[50%] bg-[var(--background-tertiary)]">
                        <img :src="react.url" alt="" class="w-5 h-5 block object-contain indent-[-9999px]">
                    </div>
                </div>
                
            </div>
            <div class="group">
                <div
                    v-for="(item, index) in options"
                    :key="index"
                    @click="item.slug ? opt_functions[item.slug]() : null"
                    class="item flex min-h-8 items-center px-2 py-1.5 justify-between mx-0 my-0.5 rounded-[2px] text-[13px] font-medium leading-[18px] cursor-pointer outline-0 text-[var(--interactive-normal)] border-[var(--interactive-normal)] text-left hover:text-[var(--white)]"
                    :class="{'hover:bg-[var(--menu-item-default-active-bg)]': item.type === 'normal', 'text-[var(--status-danger)]': item.type === 'danger', 'hover:bg-[var(--menu-item-danger-active-bg)]': item.type === 'danger'}"
                    >
                    <div class="label relative flex-auto whitespace-nowrap overflow-hidden text-ellipsis outline-0">{{ item.name }}</div>
                    <div class="iconContainer relative h-[18px] w-[18px] flex-auto grow-0 shrink-0 ml-2 outline-0">
                        <font-awesome-icon :icon="item.icon"
                                            class="block h-[16px] w-[16px] object-contain" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
const ws = inject('chat-socket')

const props = defineProps({
    cid: Number
})

const recent_reactions = ref([
    {
        'name': 'Heart',
        'url': '/static/Message/Emoji/svg/heart.svg'
    },
    {
        'name': 'Fire',
        'url': '/static/Message/Emoji/svg/fire.svg'
    },
    {
        'name': 'Joy',
        'url': '/static/Message/Emoji/svg/joy.svg'
    },
    {
        'name': 'Thumb',
        'url': '/static/Message/Emoji/svg/thumb.svg'
    },
])

const options = ref([
    {
        'name': 'Edit Message',
        'type': 'normal',
        'icon': ['fas', 'pen']
    },
    {
        'name': 'Copy Text',
        'type': 'normal',
        'icon': ['fas', 'clipboard']
    },
    {
        'name': 'Copy Message Link',
        'type': 'normal',
        'icon': ['fas', 'paperclip']
    },
    {
        'name': 'Delete Message',
        'slug': 'delete_message',
        'type': 'danger',
        'icon': ['fas', 'trash']
    }
])

const deleteMsg = (cid) => {
    if (cid == -1) return
    const d = { 'command': 'delete_message', 'cid': props.cid }
    ws.value.send(JSON.stringify(d))
}



const opt_functions = ref({
    'delete_message': deleteMsg
})

</script>

<style lang="scss">

</style>

<style lang="scss" scoped>

</style>