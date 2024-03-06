<template>
    <li class="messageListItem group my-0 border-1 border-solid border-white min-h-1 hover:bg-[#2e3035] w-full outline-none relative">
        <div
             class="message select-text break-words relative pr-12 py-[0.125rem] pl-[72px] min-h-[2.75rem] mt-[1.0625rem]">
            <div class="message-contents static ml-0 pl-0 indent-0">
                <img src=""
                     alt=""
                     class="avatar pointer-events-auto [alt]:indent-[-9999px] absolute left-4 mt-[calc(4px-0.125rem)] w-10 h-10 rounded-[50%] overflow-hidden cursor-pointer select-none z-[1]">
                <h3
                    class="header overflow-hidden relative leading-[1.375rem] text-[hsl( 214 calc( 1 * 8.1%) 61.2% / 1)] whitespace-break-spaces">
                    <span class="messageUsername mr-1">
                        <span
                              class="username text-base leading-[1.375rem] font-medium text-[hsl( 220 calc( 1 * 13%) 95.5% / 1)] inline align-baseline relative overflow-hidden">kiswelrg
                        </span>
                    </span>
                    <div
                         class="timestamp text-xs leading-[1.375rem] text-text-muted align-baseline ml-1 inline-block h-6 cursor-default pointer-events-none font-medium">
                        <time class="message-timestamp">
                            <i class="separator">14:20</i>
                        </time>
                    </div>
                </h3>
                <div
                     class="message-content pl-[72px] -ml-[72px] select-text overflow-hidden relative indent-0 text-base leading-[1.375rem] whitespace-break-spaces break-words text-[color:hsl( 210 calc( 1 * 9.1%) 87.1% / 1)]  font-light">
                    <a class="message-text anchor"><span>some link</span></a>
                    <span class="message-text normal">some text</span>
                    <span
                          class="timestamp text-xs leading-[1.375rem] text-text-muted align-baseline inline-block h-6 cursor-default pointer-events-none font-light">
                        <span class="edited text-625 select-none mx-1">(edited)</span>
                    </span>
                </div>
            </div>
            <div class="accessories empty:hidden h-fit indent-0 min-h-0 min-w-0 py-[0.125rem] relative"></div>
            <div class="buttonContainer absolute top-0 right-0">
                <!-- if isGroupTop -top-16px -->
                <div
                     class="buttons z-[1] isGroupHead -top-[25px] absolute right-0 py-0 pl-8 pr-[14px] opacity-0 group-hover:opacity-1">
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
                             class="button z-10 text-interactive-normal hover:bg-msgbutton-hover flex items-center justify-center h-6 p-1 min-w-6 flex-zauto cursor-pointer relative box-content pointer-events-auto">
                            <font-awesome-icon :icon="['fas', 'ellipsis-h']"
                                               class="block h-5 w-5 object-contain" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </li>

</template>

<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
defineProps({
  msg: Object,
})

</script>

<style lang="scss" scoped>
/* Define a custom class with the --elevation-stroke variable */
.isGroupHead {
    top: -16px;
}

.group:hover .buttons {
    @apply opacity-100;
}

.buttonlist-shadow {
    --elevation-stroke: 0 0 0 1px hsl(0 calc(1 * 0%) 0.8% / 0.15);
    box-shadow: var(--elevation-stroke);
}


</style>