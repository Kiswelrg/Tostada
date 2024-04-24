<template>
    <div class="tooltypical z-[2] flex flex-col justify-between h-full w-full text-white">
        
        <div class="toolbody flex flex-col flex-1 overflow-y-auto w-full">
            <ToolHead :title="toolDetail?.name" :intro="toolDetail?.description + ' id: ' + selectedToolId" class="flex-none"/>
            <div class="belly w-full overflow-y-auto flex-1">
                <div class="introduction">
                    <div class="introwrapper flex flex-col items-left text-left">
                        <div v-if="!intro?.length" class="paragraph px-2 py-1 bg-[#2d2d2d] rounded-md mx-2 text-1s my-1">
                            Another option you have is choosing the number of syllables in the words you speak. You probably have never considered this option before, but you have it every time you open your mouth and speak. You make so many choices like this that you never even think about, but you have the choice with each one. What are you going to do with this knowledge?
                        </div>
                        <div v-for="ito in filtered_intro" :key="ito" class="paragraph px-4 py-4 bg-[#2d2d2d] rounded-md mx-2 text-1s my-1">
                            <div v-for="content in ito.content" :key="content">{{ content }}</div>
                        </div>
                    </div>
                </div>
                <div class="toolmenu"></div>
                <div class="chat">
                    <div class="chat-wrapper text-left">
                        <div class="scroller">
                            <div class="scroller-content">
                                <ol class="messages-container">
                                    <Message v-for="m in messages" v-bind:key="m.id" :msg="m"></Message>
                                </ol>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <InputKing class="flex-none" :tool-detail="toolDetail"/>
    </div>

</template>

<script setup>
import InputKing from '@/i/Global/InputKing/InputKing.vue'
import ToolHead from '../../ToolHead/ToolHead.vue'
import { ref, computed, watch } from 'vue'
import { inject } from 'vue'
import Message from '../../Components/Message.vue'
import ToolDetail from '../../ToolDetail.vue'
const props = defineProps([
    'tool-detail',
    'introToMsg'
])

const selectedToolId = computed(() => {
    return props.toolDetail?.cid
})

const intro = computed(() => {
    if (props.toolDetail)
        return props.toolDetail['additional']['intro']
    return undefined
})

const filtered_intro = computed(() => {
    if (props.toolDetail)
        return props.toolDetail['additional']['intro']?.filter(obj => !obj.hasOwnProperty('type'))
    return undefined
})

const methods = computed(() => {
    if (props.toolDetail === undefined) return undefined
    if ('methods' in props.toolDetail) return props.toolDetail.methods
})


const messages = ref([
    {
        'a': 1,
        'id': 2,
        'isGroupHead': true,
        'avatar_src': '/static/@me/1F955.svg'
    },
    {
        'a': 1,
        'id': 3,
        'isGroupHead': false,
        'avatar_src': '/static/@me/1F955.svg'
    },
    {
        'a': 1,
        'id': 3,
        'isGroupHead': false,
        'avatar_src': '/static/@me/1F955.svg'
    },
    {
        'a': '<div style="color: red"> plain html element</div>',
        'id': 4,
        'isGroupHead': true,
        'avatar_src': '/static/@me/1F955.svg'
    },
])

watch(filtered_intro, (newV) => {
    props.introToMsg(newV)
})



</script>

<style lang="scss" scoped>
.belly {
    &::-webkit-scrollbar {
        background-color: transparent;
        width: 12px;
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
/* Define a custom class with the --elevation-stroke variable */
.group:hover .buttons {
    @apply opacity-100;
}

.buttonlist-shadow {
  --elevation-stroke: 0 0 0 1px hsl(0 calc(1 * 0%) 0.8% / 0.15);
  box-shadow: var(--elevation-stroke);
}

</style>