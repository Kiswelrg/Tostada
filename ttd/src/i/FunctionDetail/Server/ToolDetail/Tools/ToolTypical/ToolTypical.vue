<template>
    <div class="tooltypical z-[2] flex flex-col justify-between h-full w-full text-white">
        
        <div class="toolbody flex flex-col flex-1 overflow-y-auto w-full">
            <ToolHead :title="toolDetail?.name" :intro="toolDetail?.description + ' id: ' + selectedToolId" class="flex-none"/>
            <div class="belly flex-1 flex flex-col justify-end w-full overflow-y-auto">
                <Welcome :tool-detail="props.toolDetail"></Welcome>
                <div class="introduction hidden">
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

                                    <Message v-for="m in messagedIntro" v-bind:key="m.id" :msg="m"></Message>
                                    <Message v-for="m in sortedMessages" v-bind:key="m.id" :msg="m"></Message>
                                </ol>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        
            <div class="w-full h-3 block invisible"></div>
        </div>
        
        <InputKing class="flex-none" :tool-detail="toolDetail" @add-message="onAddMessage"/>
    </div>

</template>

<script setup>
import InputKing from '@/i/Global/InputKing/InputKing.vue'
import ToolHead from '../../ToolHead/ToolHead.vue'
import Welcome from '../../Welcome/Welcome.vue'
import { ref, computed, watch } from 'vue'
import Message from '../../Components/Message/Message.vue'
import { useWatchOnce } from '@/util/watcher'
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
    if (props.toolDetail){
        return props.toolDetail['additional']['intro']?.filter(obj => !obj.hasOwnProperty('type'))
    }
    return undefined
})

const messagedIntro = computed(() => {
    let r = []
    if (props.toolDetail){
        let intros = props.toolDetail['additional']['intro']?.filter(obj => !obj.hasOwnProperty('type'))
        for (const i in intros) {
            let ito = intros[i]
            r.push({
                'nickname': 'Kiswelrg',
                'date_sent': '2024-02-21T02:26:27Z',
                'id': 0,
                'isEdited': {
                    'state': false,
                    'text': 'edited'
                },
                'contents': ito.content.map(obj => ({
                    'type': 'Text',
                    'content': obj
                })),
                'isGroupHead':  i == 0 ? true : false,
                'avatar_src': '/static/@me/1F955.svg'
            })
        }
        return r
    }
    return undefined
})


const messages = ref([
    {
        'nickname': 'Kiswelrg',
        'date_sent': '2024-02-21T02:26:27Z',
        'id': 438597598,
        'isEdited': {
            'state': true,
            'text': 'edited'
        },
        'contents': [
            {
                'type': 'Text',
                'content': 'Welcome to ',
            },
            {
                'type': 'Link',
                'display_name': 'Tostada.com',
                'url': '#'
            }, 
            {
                'type': 'Text',
                'content': ', start using tools by sending messages!',
            }
        ],
        'isGroupHead': true,
        'avatar_src': '/static/@me/1F955.svg'
    }
])


const sortedMessages = computed(() => {
    if (!messages || !messages.value || !messages.value.length) return []
    return messages.value.toSorted((a,b) => {
        const d1 = new Date(a['date_sent'])
        const d2 = new Date(b['date_sent'])
        return d1 - d2
    })
})


watch(filtered_intro, (newV) => {
    props.introToMsg(newV)
})


const onAddMessage = (l) => {
    messages.value.push(l)
}

const chatSocket = ref(undefined)
const { stopped, stopWatcher } = useWatchOnce(() => props.toolDetail,
  (newValue, old) => {
    if (newValue !== undefined && newValue.cid !== undefined) {
        const urlString = import.meta.env.VITE_BACKEND_URL;
        const url = new URL(urlString);
        chatSocket.value = new WebSocket(
            `ws://${url.host}/ws/chat/${newValue.cid}/`
        )
        chatSocket.value.onopen = function(e) {
            console.log("WebSocket connection established");
        };
        return true
    }
    return false
  }
)


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