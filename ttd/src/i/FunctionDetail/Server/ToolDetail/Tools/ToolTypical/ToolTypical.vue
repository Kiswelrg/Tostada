<template>
    <div class="tooltypical z-[2] flex flex-col justify-between h-full w-full text-white">
        
        <div class="toolbody flex flex-col h-[calc(100%-53px)]">
            <ToolHead :title="tool.title" :intro="tool.intro"/>
            <div class="belly overflow-y-auto">
                <div class="introduction">
                    <div class="introwrapper flex flex-col items-left text-left">
                        <div class="paragraph px-2 py-1 bg-[#2d2d2d] rounded-md mx-2 text-1s my-1">
                            Another option you have is choosing the number of syllables in the words you speak. You probably have never considered this option before, but you have it every time you open your mouth and speak. You make so many choices like this that you never even think about, but you have the choice with each one. What are you going to do with this knowledge?
                        </div>
                        <div class="paragraph px-2 py-1 bg-[#2d2d2d] rounded-md mx-2 text-1s my-1">
                            Love isn't always a ray of sunshine. That's what the older girls kept telling her when she said she had found the perfect man. She had thought this was simply bitter talk on their part since they had been unable to find true love like hers. But now she had to face the fact that they may have been right. Love may not always be a ray of sunshine. That is unless they were referring to how the sun can burn.
                        </div>
                    </div>
                </div>
                <div class="toolmenu"></div>
                <div class="chat">
                    <div class="chat-wrapper text-left">
                        <div class="scroller">
                            <div class="scroller-content">
                                <ol class="messages-container">
                                    <li v-for="_ in 2" class="messageListItem group my-0 border-1 border-solid border-white min-h-1 hover:bg-[#2e3035] w-full outline-none relative">
                                        <div class="message mt-[1.0625rem] min-h-[2.75rem] pl-[2.75rem] py-[0.125rem] pr-12 relative break-words select-text">
                                            <div class="contents static ml-0 pl-0 indent-0">
                                                <img src="" alt="" class="avatar pointer-events-auto [alt]:indent-[-9999px] absolute left-4 mt-[calc(4px-0.125rem)] w-10 h-10 rounded-[50%] overflow-hidden cursor-pointer select-none z-[1]">
                                                <h3 class="header overflow-hidden relative leading-[1.375rem] text-[hsl( 214 calc( 1 * 8.1%) 61.2% / 1)] whitespace-break-spaces">
                                                    <span class="messageUsername mr-1">
                                                        <span class="username text-base leading-[1.375rem] font-medium text-[hsl( 220 calc( 1 * 13%) 95.5% / 1)] inline align-baseline relative overflow-hidden">
                                                            kiswelrg
                                                        </span>
                                                    </span>
                                                    <div class="timestamp text-xs leading-[1.375rem] text-text-muted align-baseline ml-1 inline-block h-6 cursor-default pointer-events-none font-medium">
                                                        <time class="message-timestamp">
                                                            <i class="separator">14:20</i>
                                                        </time>
                                                    </div>
                                                </h3>
                                                <div class="message-content pl-[72px] -ml-[72px] select-text overflow-hidden relative indent-0 text-base leading-[1.375rem] whitespace-break-spaces break-words text-[color:hsl( 210 calc( 1 * 9.1%) 87.1% / 1)] ">
                                                    <a class="message-text anchor"><span>some link</span></a>
                                                    <span class="message-text normal">some text</span>
                                                    <span class="timestamp text-xs leading-[1.375rem] text-text-muted align-baseline inline-block h-6 cursor-default pointer-events-none font-medium">
                                                        <span class="edited text-625 select-none">edited</span>
                                                    </span>
                                                </div>
                                            </div>
                                            <div class="accessories empty:hidden h-fit indent-0 min-h-0 min-w-0 py-[0.125rem] relative"></div>
                                            <div class="buttonContainer absolute top-0 right-0">
                                                <!-- if isGroupTop -top-16px -->
                                                <div class="buttons -top-[25px] absolute right-0 z-[1] py-0 pl-8 pr-[14px] opacity-1 group-hover:opacity-1 pointer-events-none">
                                                    <div class="buttons-wrapper bg-bg-primary buttonlist-shadow grid grid-flow-col box-border h-8 rounded items-center justify-start select-none transition-shadow duration-100 ease-out relative overflow-hidden">
                                                        <div class="button text-interactive-normal flex items-center justify-center h-6 p-1 min-w-6 flex-zauto cursor-pointer relative"><img class="object-contain w-5 h-5 block" src="@/assets/Tool/Detail/Message/Buttons/face-smile-solid.svg" alt="">
                                                        </div>
                                                        <div class="button text-interactive-normal flex items-center justify-center h-6 p-1 min-w-6 flex-zauto cursor-pointer relative"><img class="object-contain w-5 h-5 block" src="@/assets/Tool/Detail/Message/Buttons/pen-solid.svg" alt="">
                                                        </div>
                                                        <div class="button text-interactive-normal flex items-center justify-center h-6 p-1 min-w-6 flex-zauto cursor-pointer relative"><img class="object-contain w-5 h-5 block" src="@/assets/Tool/Detail/Message/Buttons/ellipsis-solid.svg" alt="">
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                </ol>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <InputKing />
    </div>

</template>

<script setup>
import InputKing from '@/i/Global/InputKing/InputKing.vue'
import ToolHead from '../../ToolHead/ToolHead.vue'
import { ref } from 'vue'
let a = '/home/wxy/prj/Tostada/ttd/src/assets/Tool/Detail/Message/Buttons/pen-solid.svg'
const tool = ref({
    title: 'tool',
    intro: 'this is an introduction'
})
</script>

<style lang="scss" scoped>
/* Define a custom class with the --elevation-stroke variable */
.buttonlist-shadow {
  --elevation-stroke: 0 0 0 1px hsl(0 calc(1 * 0%) 0.8% / 0.15);
  box-shadow: var(--elevation-stroke);
}

</style>