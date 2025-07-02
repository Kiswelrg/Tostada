<template>
    <div class="tooltypical z-[2] flex flex-col justify-between h-full w-full text-white">

        <div>
            <ToolHead 
                ref="toolHeadRef"
                :title="toolDetail?.name" 
                :intro="toolDetail?.description" 
                :tool-detail="toolDetail"
                @search-results="handleSearchResults"
                @search-cleared="handleSearchCleared"
                @search-focused="handleSearchFocused"
                class="flex-none" />
        </div>

        <div class="toolbody flex flex-1 overflow-hidden w-full">
            <!-- Main chat area -->
            <div class="chat-area flex flex-col flex-1 overflow-y-auto w-full">
                <div class="belly flex-1 flex flex-col justify-end w-full overflow-auto">
                    <div class="belly-detail w-full h-fit overflow-y-scroll pb-3" ref="belly" @scroll="onBellyScroll">
                        <Welcome :tool-detail="props.toolDetail"></Welcome>
                        <div class="introduction hidden">
                            <div class="introwrapper flex flex-col items-left text-left">
                                <div v-if="!intro?.length"
                                    class="paragraph px-2 py-1 bg-[#2d2d2d] rounded-md mx-2 text-1s my-1">
                                    Another option you have is choosing the number of syllables in the words you speak. You
                                    probably have never considered this option before, but you have it every time you open
                                    your mouth and speak. You make so many choices like this that you never even think
                                    about, but you have the choice with each one. What are you going to do with this
                                    knowledge?
                                </div>
                                <div v-for="ito in filtered_intro" :key="ito"
                                    class="paragraph px-4 py-4 bg-[#2d2d2d] rounded-md mx-2 text-1s my-1">
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

                                            <Message v-for="m in messagedIntro" v-bind:key="m.id" :msg="m" @attachment-deleted="handleAttachmentDeleted"></Message>
                                            <Message v-for="(m, idx) in sortedMessages" :is-group-head="isMsgHead(idx)"
                                                v-bind:key="m.id" :msg="m" @attachment-deleted="handleAttachmentDeleted"></Message>
                                        </ol>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="w-full h-1 block hidden"></div>

                <InputKing class="flex-none" :tool-detail="toolDetail" :chat-socket="chatSocket" @add-message="onAddMessage"
                    :input-bar-info="inputBarInfo" />
            </div>

            <!-- Search results area -->
            <div v-if="showSearchResults" class="search-area w-96 flex-shrink-0 border-l border-[#404249]">
                <SearchResults 
                    :search-data="searchData"
                    :tool-detail="toolDetail"
                    @jump-to-message="handleJumpToMessage"
                    @page-change="handlePageChange" />
            </div>
        </div>
    </div>

</template>

<script setup>
import InputKing from '@/i/Global/InputKing/InputKing.vue'
import ToolHead from '../../ToolHead/ToolHead.vue'
import Welcome from '../../Welcome/Welcome.vue'
import SearchResults from './SearchResults.vue'
import { ref, computed, watch, inject, nextTick } from 'vue'
import Message from '../../Components/Message/Message.vue'
import { useWatchOnce } from '@/util/watcher'
import { jsonWithBigInt } from '@/util/parse'
import { getCookie } from '@/util/session'
const chatSocket = inject('chat-socket')
const layerB = inject('layer-b')
const belly = ref()
const scrollInfo = ref({})
const showSearchResults = ref(false)
const searchData = ref({
    query: '',
    results: [],
    totalCount: 0,
    currentPage: 1,
    totalPages: 0
})
const toolHeadRef = ref(null)
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

        const diff2bottom = Math.floor(scrollTop + clientHeight) - Math.ceil(scrollHeight)
        if (diff2bottom >= -2 && diff2bottom <= 2) {
            // console.log('At the bottom of the div');
            opt = 2;
            // Load newer messages when scrolled to bottom
            if (!isLoadingMore.value && newestMessageId.value) {
                loadMoreMessages('newer')
            }
        } else if (scrollTop === 0) {
            // console.log('At the top of the div');
            opt = 0;
            // Load older messages when scrolled to top
            if (!isLoadingMore.value && oldestMessageId.value) {
                loadMoreMessages('older')
            }
        }
        return [opt, scrollTop, clientHeight, scrollHeight]
    }
    return undefined
}

const selectedToolId = computed(() => {
    return props.toolDetail?.cid
})

const intro = computed(() => {
    if (props.toolDetail && props.toolDetail['additional'] && props.toolDetail['additional']['intro'])
        return props.toolDetail['additional']['intro']
    return undefined
})

const filtered_intro = computed(() => {
    try {
        if (props.toolDetail) {
            return props.toolDetail['additional']['intro']?.filter(obj => !obj.hasOwnProperty('type'))
        }

    }
    catch (e) {
        return undefined
    }
    return undefined
})


const messagedIntro = computed(() => {
    let r = []
    if (props.toolDetail && props.toolDetail['additional'] && props.toolDetail['additional']['intro']) {
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
                'contents': {
                    'version': '0.10.0',
                    'block': [{'type': 'text', 'content': ito.content.join('\n')}]
                },
                'isGroupHead': i == 0 ? true : false,
                'avatar_src': '/static/@me/1F955.svg'
            })
        }
        return r
    }
    return undefined
})


const messages = ref([])
const processedMessageIds = new Set()

// Pagination configuration - matches backend config
const INITIAL_LIMIT = 50  // A messages for initial load
const PAGINATION_LIMIT = 30  // B messages for pagination  
const MAX_CACHE_SIZE = 200  // Maximum messages to keep in cache
const isLoadingMore = ref(false)


const sortedMessages = computed(() => {
    if (!messages || !messages.value || !messages.value.length) return []
    return messages.value.slice().sort((a, b) => {
        // const d1 = new Date(a['time_sent'])
        // const d2 = new Date(b['time_sent'])
        return a['cid'] > b['cid'] ? 1 : a['cid'] < b['cid'] ? -1 : 0
    })
})

const oldestMessageId = computed(() => {
    return sortedMessages.value.length > 0 ? sortedMessages.value[0].cid : null
})

const newestMessageId = computed(() => {
    return sortedMessages.value.length > 0 ? sortedMessages.value[sortedMessages.value.length - 1].cid : null
})

// Load more messages function
const loadMoreMessages = (direction) => {
    if (isLoadingMore.value || !chatSocket.value) return

    isLoadingMore.value = true
    const payload = {
        command: 'fetch_more_messages',
        direction: direction,
        limit: PAGINATION_LIMIT
    }

    if (direction === 'older' && oldestMessageId.value) {
        payload.oldest_cid = oldestMessageId.value.toString()
    } else if (direction === 'newer' && newestMessageId.value) {
        payload.newest_cid = newestMessageId.value.toString()
    }

    chatSocket.value.send(JSON.stringify(payload))
}
// Trim messages to maintain cache size
const trimMessages = (direction) => {
    if (messages.value.length <= MAX_CACHE_SIZE) return
    const sorted = messages.value.slice().sort((a, b) => a['cid'] > b['cid'] ? 1 : a['cid'] < b['cid'] ? -1 : 0)
    if (direction === 'older') {
        // Remove newest messages when loading older ones
        const toKeep = sorted.slice(0, MAX_CACHE_SIZE)
        messages.value = toKeep
    } else if (direction === 'newer') {
        // Remove oldest messages when loading newer ones  
        const toKeep = sorted.slice(-MAX_CACHE_SIZE)
        messages.value = toKeep
    }
}

const deleteMsg = (cid) => {
    const index = messages.value.findIndex(msg => msg.cid === cid);
    if (index !== -1) {
        messages.value.splice(index, 1);
    }
}

const handleAttachmentDeleted = (attachmentCID, messageCID) => {
    // Find the message and remove the attachment from its attachments array
    const message = messages.value.find(msg => msg.cid === messageCID)
    if (message && message.attachments) {
        message.attachments = message.attachments.filter(attachment => {
            const match = attachment.url.match(/\/(\d+)\/(\d+)\//)
            if (match) {
                const extractedCID = match[2]
                return extractedCID !== attachmentCID
            }
            return true
        })
    }
}

const handleAttachmentDeletedWS = (attachmentCID, messageCID) => {
    // Handle WebSocket-based attachment deletion (for real-time updates from other users)
    handleAttachmentDeleted(attachmentCID, messageCID)
}

const handleSearchResults = (data) => {
    searchData.value = data
    // Show search results area when we have search data
    showSearchResults.value = true
}

const handleSearchCleared = () => {
    showSearchResults.value = false
    searchData.value = {
        query: '',
        results: [],
        totalCount: 0,
        currentPage: 1,
        totalPages: 0
    }
}

const handleSearchFocused = () => {
    // Show search area with previous results if we have any
    if (searchData.value.results.length > 0) {
        showSearchResults.value = true
    }
}

const handlePageChange = async (page) => {
    // Use the proper component reference to trigger search for specific page
    if (toolHeadRef.value && toolHeadRef.value.performSearch) {
        await toolHeadRef.value.performSearch(searchData.value.query, page)
    }
}

const handleJumpToMessage = (messageResult) => {
    // Find the message in the current messages array and scroll to it
    const messageElement = document.querySelector(`[data-message-id="${messageResult.id}"]`)
    if (messageElement) {
        messageElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
        // Optionally highlight the message
        messageElement.classList.add('highlight-message')
        setTimeout(() => {
            messageElement.classList.remove('highlight-message')
        }, 3000)
    } else {
        // If message is not in current view, we might need to load it
        console.log('Message not found in current view, might need to load:', messageResult)
    }
}


watch(filtered_intro, (newV) => {
    props.introToMsg(newV)
})


const onAddMessage = (l) => {
    // scrollInfo.value = onBellyScroll();
    if (messages.value.includes(l)) return
    messages.value = [...messages.value, l]
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
    const oldSender = oldM['sender']?.username || 'Account Deleted'
    const newSender = newM['sender']?.username || 'Account Deleted'
    return oldSender === newSender && isTimeClose(oldM['time_sent'], newM['time_sent'])
}

const isMsgHead = (idx) => {
    return idx == 0 || !isMsgsClose(sortedMessages.value[idx - 1], sortedMessages.value[idx])
}


const connect = (url, tool) => {
    const getWsHost = (url) => {
        const host = window.location.hostname; // new URL(url).host;
        if (
            host === "127.0.0.1" || host === "localhost" ||
            /^192\.168\.\d{1,3}\.\d{1,3}$/.test(host)
        ) {
            const port = import.meta.env.VITE_LAN_PORT ? import.meta.env.VITE_LAN_PORT : (new URL(import.meta.env.VITE_BACKEND_URL)).port;
            return `${host}:${port}`;//
        }
        return import.meta.env.VITE_WS_HOST;
    };
    const ws_url = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${getWsHost(url)}/ws/chat/${tool.cid}/`
    // console.log('Vue Backend Host:', url.host, 'ws_url:', ws_url, import.meta.env)
    if (chatSocket.value !== undefined) {
        chatSocket.value.onclose = function (e) { }
        chatSocket.value.close()
    }
    chatSocket.value = new WebSocket(
        ws_url
    )
    chatSocket.value.onopen = function (e) {
        console.log("WS/CHAT connection established")
        reconnectAttempts.value = 0
    }
    chatSocket.value.onmessage = function (e) {
        const data = jsonWithBigInt(e.data)
        console.log('Got messages: ')
        if (data['type'] == 'chat_message') {
            // scrollInfo.value = onBellyScroll();
            const cur = data['messages'];
            console.log(cur.map(a => a['attachments'].length ? a['attachments'] : undefined));
            // messages.value.push.apply(messages.value, cur);
            if (!messages.value.includes(cur))
                messages.value = [...messages.value, ...cur]
        } else if (data['type'] == 'attachment_deleted') {
            console.log('attachment deletion:', data)
            // Handle WebSocket attachment deletion
            handleAttachmentDeletedWS(data.attachment_cid, data.message_cid)
        }
        else if (data['type'] == 'message_deleted') {
            deleteMsg(data.cid);
        }
        else if (data['type'] == 'history_message') {
            // Initial message load
            console.log('Initial messages loaded:', data)
            messages.value = data['messages']
            let logs = [];
            messages.value.map((a) => {
                if (a['attachments'].length)
                    logs.push.apply(logs, a['attachments']);
            })
            // Scroll to bottom for initial load
            nextTick(() => {
                belly.value.scrollTop = belly.value.scrollHeight - belly.value.clientHeight;
            })
        }
        else if (data['type'] == 'paginated_messages') {
            // Handle paginated message loads
            console.log('Paginated messages loaded:', data)
            const direction = data['direction']
            const newMessages = data['messages']

            if (newMessages.length > 0) {
                // Store current scroll position for older messages
                const wasAtBottom = direction === 'newer'
                let savedScrollPos = null
                if (direction === 'older') {
                    savedScrollPos = belly.value.scrollHeight - belly.value.scrollTop
                }

                // Optimized merge with built-in bounds checking
                const mergedMessages = mergeLists(newMessages)
                messages.value = mergedMessages
                // Trim cache after adding new messages
                trimMessages(direction)
                // Restore scroll position
                nextTick(() => {
                    if (direction === 'older' && savedScrollPos) {
                        belly.value.scrollTop = belly.value.scrollHeight - savedScrollPos
                    } else if (direction === 'newer' && wasAtBottom) {
                        belly.value.scrollTop = belly.value.scrollHeight - belly.value.clientHeight
                    }
                })
            }

            isLoadingMore.value = false
        }
        else if (data['type'] == 'chat_message_delete') {
        }
    }

    chatSocket.value.onclose = function (e) {
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

    chatSocket.value.onerror = function (error) {
        console.error('WebSocket Error: ', error)
    }
}


const onMessageChange = watch(messages, (newValue, old) => {
    console.log('Messages changed', scrollInfo.value)
    scrollInfo.value = onBellyScroll()
    nextTick(() => {
        console.log('Messages changed2', scrollInfo.value)
        if (scrollInfo.value !== undefined) {
            if (scrollInfo.value == {} || scrollInfo.value[0] === 2) {
                console.log('messages updated, now scroll', belly.value.scrollTop, belly.value.scrollHeight, belly.value.clientHeight)
                belly.value.scrollTop = belly.value.scrollHeight - belly.value.clientHeight;
            }
        }
    })

})


const onToolDetailChange = watch(() => props.toolDetail, (newValue, old) => {
    // clear messages if channel changes
    messages.value = []
    if (newValue.class !== 'ChannelOfChat') {
        return
    }
    if (newValue !== undefined && newValue.cid !== undefined) {
        const urlString = import.meta.env.VITE_BACKEND_URL
        const url = new URL(urlString)
        connect(url, newValue)
        return true
    }
    return false
})


const inputBarInfo = computed(() => {
    const chat_allowed = [
        'ChannelOfChat'
    ]
    const enable = props.toolDetail ? chat_allowed.includes(props.toolDetail.class) : false
    return {
        'enable': enable,
        'placeholder': enable ? 'Message Here...' : 'This is a voice channel and currently under development.'
    }
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
        border: 2px solid rgba(0, 0, 0, 0);
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

.highlight-message {
    @apply bg-yellow-400 bg-opacity-20 transition-colors duration-300;
}
</style>
