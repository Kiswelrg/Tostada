<template>
    <li class="messageListItem group my-0 border-1 border-solid border-white min-h-1 hover:bg-[#2e3035] w-full outline-none relative">
        <div
            class="message select-text break-words relative pr-12 py-[0.125rem] pl-[72px] mt-0"
            :class="{'mt-[1.0625rem]': props.isGroupHead, 'min-h-[1.375rem]': !props.isGroupHead, 'min-h-[2.75rem]': props.isGroupHead}"
            >
            <div class="message-contents static ml-0 pl-0 indent-0">
                <img 
                    v-if="props.isGroupHead"
                    :src="userAvatarUrl"
                    alt=""
                    class="avatar pointer-events-auto [alt]:indent-[-9999px] absolute left-4 mt-[calc(4px-0.125rem)] w-10 h-10 rounded-[50%] overflow-hidden cursor-pointer select-none z-[1]"
                    
                    >
                <h3
                    v-if="props.isGroupHead"
                    class="header overflow-hidden relative leading-[1.375rem] text-[hsl( 214 calc( 1 * 8.1%) 61.2% / 1)] whitespace-break-spaces">
                    <span class="messageUsername mr-1">
                        <span
                              class="username text-base leading-[1.375rem] font-medium text-[hsl( 220 calc( 1 * 13%) 95.5% / 1)] inline align-baseline relative overflow-hidden">{{ props.msg.sender.username }}
                        </span>
                    </span>
                    <div
                         class="timestamp text-xs leading-[1.375rem] text-text-muted align-baseline ml-1 inline-block h-6 cursor-default pointer-events-none font-medium">
                        <time class="message-timestamp">
                            <i class="separator">{{ detailedTime }}</i>
                        </time>
                    </div>
                </h3>

                <span v-if="!props.isGroupHead" class="compact-timestamp text-[11px] inline-block opacity-0 indent-0 font-text-muted mr-1 text-right select-none w-14 h-[1.375rem] left-0 absolute">
                    <time title="Today at 12:39 PM" datetime="2024-03-15T04:39:20.353Z" class="pointer-events-none indent-0 text-text-muted text-right select-none leading-[22px]">{{ time_XM }}</time>
                </span>

                <div
                    class="message-content pl-[72px] -ml-[72px] select-text overflow-hidden relative indent-0 text-base leading-[1.375rem] whitespace-break-spaces break-words text-[color:hsl( 210 calc( 1 * 9.1%) 87.1% / 1)]  font-light">
                    
                    <!-- <component v-for="(item, index) in msg['contents']" :key="index" :is="tabs[item['type']]" :msg-item="item" class="text-[color:var(--text-normal)] text-3s"></component> -->
                    <component :is="tabs['Text']" :msg-item="{'type':'Text','content':msg.contents}" class="text-[color:var(--text-normal)] text-3s"></component>

                    <Edited v-if="msg['is_edited']['state']" :is-edited="msg['is_edited']"></Edited>
                </div>
            </div>

            <!-- Reactions / Attachments -->
            <Accessories :attachments="msg.attachments"></Accessories>

            <!-- Actions -->
            <div class="buttonContainer absolute top-0 right-0">
                <!-- if isGroupTop -top-16px -->
                <div
                     class="buttons z-[1] absolute right-0 py-0 pl-8 pr-[14px] opacity-0 group-hover:opacity-1"
                     :class="{'-top-[16px]': props.isGroupHead, '-top-[25px]': !props.isGroupHead}"
                     >
                    <div
                         class="buttons-wrapper bg-msgbutton-primary buttonlist-shadow grid grid-flow-col box-border h-8 rounded items-center justify-start select-none transition-shadow duration-100 ease-out relative overflow-hidden z-10">
                        <div
                             class="button z-10 text-interactive-normal hover:bg-msgbutton-hover flex items-center justify-center h-6 p-1 min-w-6 flex-zauto cursor-pointer relative box-content pointer-events-auto">
                            <font-awesome-icon :icon="['fas', 'smile']"
                                               class="block h-5 w-5 object-contain text-red" />
                        </div>
                        <div
                             class="button z-10 text-interactive-normal hover:bg-msgbutton-hover flex items-center justify-center h-6 p-1 min-w-6 flex-zauto cursor-pointer relative box-content pointer-events-auto">
                            <font-awesome-icon :icon="['fas', 'pen']"
                                               class="block h-5 w-5 object-contain text-red" />
                        </div>
                        <div
                            @click.stop="openMsgMenu($event, msg.cid)"
                             class="button z-10 text-interactive-normal hover:bg-msgbutton-hover flex items-center justify-center h-6 p-1 min-w-6 flex-zauto cursor-pointer relative box-content pointer-events-auto">
                            <font-awesome-icon :icon="['fas', 'ellipsis-h']"
                                               class="block h-5 w-5 object-contain"
                                               />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </li>

</template>

<script setup>
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { computed, shallowRef, ref, inject } from 'vue'
import Edited from './Content/Edited.vue'
import Link from './Content/Link.vue'
import Text from './Content/Text.vue'
import Accessories from './Accessories/Accessories.vue'

const props = defineProps({
  msg: Object,
  isGroupHead: Boolean
})

const backend_url = () => {
    return import.meta.env.VITE_BACKEND_URL
}

const userAvatarUrl = computed(() => {
    if (props.msg.sender === undefined || props.msg.sender.avatar == '' || props.msg.sender.avatar == '#') return '/static/tool/main/user-solid.svg'
    return props.msg.sender.avatar + '?size=128'
})

const layerB = inject('layer-b')

const tabs = shallowRef({
    'Text': Text,
    'Link': Link,
    'Edited': Edited
})


// const is_group_head = computed(() => {
//     return props.msg?.value?.is_group_head ?? false
// })

const time = computed(() => {
    if (!props.msg || !props.msg['time_sent']) return ''
    const d = new Date(props.msg['time_sent'])
    return `${d.getHours()}:${d.getMinutes()}`
})

const time_XM = computed(() => {
    if (!props.msg || !props.msg['time_sent']) return ''
    const d = new Date(props.msg['time_sent'])
    const m = d.getHours() >= 12 ? 'P' : 'A'
    return `${d.getHours()}:${d.getMinutes()} ${m}M`
})


function formatDate(date) {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  const options = { hour: 'numeric', minute: 'numeric', hour12: true };
  const timeString = date.toLocaleTimeString('en-US', options);

  if (date >= today) {
    return `Today at ${timeString}`;
  } else if (date >= yesterday) {
    return `Yesterday at ${timeString}`;
  } else {
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const year = date.getFullYear();
    return `${month}/${day}/${year} ${timeString}`;
  }
}


const detailedTime = computed(() => {
    const d = new Date(props.msg.time_sent)
    return formatDate(d)
})

const openMsgMenu = (e, cid) => {
    layerB.value.open('MsgMenu', e.currentTarget, cid);
}


const temp_attach = (msg) => {
    return msg.attachments.map(a => `name: ${a.name}, url: ${import.meta.env.VITE_BACKEND_URL}${a.url}`)
}

</script>

<style lang="scss">
:root {
    --text-normal: hsl( 210 calc( 1 * 9.1%) 87.1% / 1);
}

</style>


<style lang="scss" scoped>
/* Define a custom class with the --elevation-stroke variable */
.is_group_head {
    top: -16px;
}

.group:hover {
    .buttons, .compact-timestamp {
        @apply opacity-100;
    }

}

.buttonlist-shadow {
    --elevation-stroke: 0 0 0 1px hsl(0 calc(1 * 0%) 0.8% / 0.15);
    box-shadow: var(--elevation-stroke);
}


</style>