<template>
    <div class="tooltypical z-[2] flex flex-col justify-between h-full w-full text-white">
        
        <div class="toolbody flex flex-col flex-1 overflow-y-auto w-full">
            <ToolHead :title="toolDetail?.name" :intro="toolDetail?.description + '_test_jenkins'" class="flex-none"/>
            <div class="belly flex-1 flex flex-col justify-end w-full overflow-auto">
                <div class="belly-detail w-full h-fit overflow-y-scroll"
                    ref="belly"
                    @scroll="onBellyScroll"
                >
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
                                        <Message v-for="(m, idx) in sortedMessages" :is-group-head="isMsgHead(idx)" v-bind:key="m.id" :msg="m"></Message>
                                    </ol>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        
            <div class="w-full h-1 block hidden"></div>
        </div>
        
        <InputKing class="flex-none" :tool-detail="toolDetail" :chat-socket="chatSocket" @add-message="onAddMessage"/>
    </div>

</template>

<script setup>
import InputKing from '@/i/Global/InputKing/InputKing.vue'
import ToolHead from '../../ToolHead/ToolHead.vue'
import Welcome from '../../Welcome/Welcome.vue'
import { ref, computed, watch, inject, nextTick } from 'vue'
import Message from '../../Components/Message/Message.vue'
import { useWatchOnce } from '@/util/watcher'
import { jsonWithBigInt } from '@/util/parse'
import { getCookie } from '@/util/session'
const chatSocket = inject('chat-socket')
const layerB = inject('layer-b')
const belly = ref()
const reconnectAttempts = ref(0)
const props = defineProps([
    'tool-detail',
    'introToMsg'
])

const onBellyScroll = () => {
    if (belly.value) {
        const scrollTop = belly.value.scrollTop;
        const scrollHeight = belly.value.scrollHeight;
        const clientHeight = belly.value.clientHeight;
        let opt = 1; // 0 top, 1 middle, 2 bottom
        // console.log('Scroll Top:', scrollTop, scrollHeight, clientHeight);

        if (scrollTop === 0) {
            // console.log('At the top of the div');
            opt = 0;
        }

        if (scrollTop + clientHeight === scrollHeight) {
            // console.log('At the bottom of the div');
            opt = 2;
        }
        return [opt, scrollTop, clientHeight, scrollHeight]
    }
    return undefined
}

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
                'is_edited': {
                    'state': false,
                    'text': 'edited'
                },
                'contents': {'type':'Text','content':ito.content.join('\n')},
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
        'sender': {
            'nickname': 'Kis',
            'username': 'Kiswelrg',
        },
        'mentioned_user': {
            'nickname': 'Kis',
            'username': 'Kiswelrg',
        },
        'tool_used': {
            'name': 'Welcome',
            'description': 'some_tool desc',
            'app_name': 'some_app'
        },
        'time_sent': '2024-02-21T02:26:27Z',
        'type': 'normal',
        'cid': 0,
        'is_edited': {
            'state': true,
            'text': 'edited',
            'last_edit': '2024-02-21T02:26:27Z'
        },
        'is_group_head': true,
        'is_private': false,
        'avatar_src': '/static/@me/1F955.svg',
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
                'content': ', start using tools by selecting a Bot at the bottom right corner and send messages!',
            }
        ],
    }
])


const sortedMessages = computed(() => {
    if (!messages || !messages.value || !messages.value.length) return []
    return messages.value.slice().sort((a,b) => {
        // const d1 = new Date(a['time_sent'])
        // const d2 = new Date(b['time_sent'])
        return a['cid'] > b['cid'] ? 1 : a['cid'] < b['cid'] ? -1 : 0
    })
})

const deleteMsg = (cid) => {
    let l = 0;
    let r = messages.value.length-1;
    while(l<=r) {
        const m = (l+r)>>1;
        const id = sortedMessages.value[m].cid
        if(cid>id) l = m+1;
        else if(cid<id) r = m-1;
        else {
            messages.value.splice(m, 1);
            return;
        }
    }
}


watch(filtered_intro, (newV) => {
    props.introToMsg(newV)
})


const onAddMessage = (l) => {
    messages.value.push(l)
}

const mergeLists = (newList) => {
    const oldList = sortedMessages.value;
    let i = 0, j = 0;
    const mergedList = [];
    const len1 = oldList.length;
    const len2 = newList.length;

    while (i < len1 && j < len2) {
        if (oldList[i].cid === newList[j].cid) {
            // If the IDs match, check time_sent
            if (oldList[i].time_sent === newList[j].time_sent) {
                mergedList.push(newList[j]);
                i++;
                j++;
            } else {
                // Handle the case where time_sent doesn't match
                // Assuming you want to skip updating in this case
                console.error(`2 msgs have identical id!`, oldList[i], newList[i])
                // and we still push the newList item into mergeList, in case the loop goes deadlock
                mergedList.push(newList[j]);
                j++;
            }
        } else if (oldList[i].time_sent < newList[j].time_sent) {
            mergedList.push(oldList[i]);
            i++;
        } else {
            mergedList.push(newList[j]);
            j++;
        }
    }

    // Add remaining items from oldList
    while (i < len1) {
        mergedList.push(oldList[i]);
        i++;
    }

    // Add remaining items from newList
    while (j < len2) {
        mergedList.push(newList[j]);
        j++;
    }
    return mergedList;
}

const isTimeClose = (oldT, newT) => {
    const d1 = new Date(oldT)
    const d2 = new Date(newT)
    const diffInMs = Math.abs(d2 - d1)
    const interval = 60 * 60 * 1000
    return diffInMs < interval
}


const isMsgsClose = (oldM, newM) => {
    return oldM['sender']['username'] === newM['sender']['username'] && isTimeClose(oldM['time_sent'], newM['time_sent'])
}

const isMsgHead = (idx) => {
    return idx == 0 || !isMsgsClose(sortedMessages.value[idx-1], sortedMessages.value[idx])
}


const connect = (url, tool) => {
    const ws_url = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${import.meta.env.DEV === 'development' ? url.host : import.meta.env.VITE_WS_HOST}/ws/chat/${tool.cid}/`
    // console.log('Vue Backend Host:', url.host, 'ws_url:', ws_url, import.meta.env)
    chatSocket.value = new WebSocket(
        ws_url
    )
    chatSocket.value.onopen = function(e) {
        console.log("WS/CHAT connection established")
        reconnectAttempts.value = 0
    }
    chatSocket.value.onmessage = function(e) {
        const data = jsonWithBigInt(e.data)
        console.log('Got messages: ')
        if (data['type'] == 'chat_message') {
            const scrollInfo = onBellyScroll();
            const cur = data['messages'];
            console.log(cur.map(a => a['attachments'].length ? a['attachments'] : undefined));
            messages.value.push.apply(messages.value, cur);
            nextTick(()=>{
                if (scrollInfo !== undefined) {
                    if (scrollInfo[0] === 2) {
                        belly.value.scrollTop = belly.value.scrollHeight - belly.value.clientHeight;
                    }
                }
            })
        }
        else if (data['type'] == 'message_deleted') {
            deleteMsg(data.cid);
        } else if (data['type'] == 'history_message') {
            const scrollInfo = onBellyScroll();
            console.log(data)
            messages.value = data['messages']
            let logs = [];
            messages.value.map((a) => {
                if (a['attachments'].length)
                    logs.push.apply(logs,a['attachments']);
            })
            // console.log(logs);
            if (scrollInfo !== undefined) {
                nextTick(()=>{
                    belly.value.scrollTop = belly.value.scrollHeight - belly.value.clientHeight;
                })
            }
        } else if (data['type'] == 'chat_message_delete') {
        }
    }

    chatSocket.value.onclose = function(e) {
        console.error('Chat socket closed unexpectedly')
        if (reconnectAttempts.value < 12) {
            const time = Math.pow(2, reconnectAttempts.value) * 1000;
            const urlString = import.meta.env.VITE_BACKEND_URL
            const url = new URL(urlString)
            console.log(`Reconnecting in ${time / 1000} seconds...`);
            setTimeout(connect, time, url, props.toolDetail);
            reconnectAttempts.value++;
        } else {
            console.error('Max reconnection attempts reached. Could not reconnect.');
        }
    }

    chatSocket.value.onerror = function(error) {
        console.error('WebSocket Error: ', error)
    }
}


const onToolDetailChange = watch(() => props.toolDetail, (newValue, old) => {
    if (newValue.class !== 'ChannelOfChat') return
    if (newValue !== undefined && newValue.cid !== undefined) {
        const urlString = import.meta.env.VITE_BACKEND_URL
        const url = new URL(urlString)
        connect(url, newValue)
        return true
    }
    return false
})


</script>

<style lang="scss" scoped>
.belly-detail {
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
