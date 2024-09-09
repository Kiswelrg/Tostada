<template>
  <div class="welcome-container m-4 flex flex-col items-start">
    <div
      class="emptychannel-icon flex justify-center items-center mt-4 h-[68px] w-[68px] rounded-full bg-[var(--background-accent)]"
    >
      <font-awesome-icon :icon="['fas', 'hashtag']" class="text-[#cbcbcb] h-4 w-4" />
    </div>
    <h3 class="my-2 text-4sdouble text-[color:var(--header-primary)] font-bold">
      Welcome to #{{ props.toolDetail?.name }}!
    </h3>
    <div
      class="description text-4s text-[var(--header-secondary)] font-normal"
    >
      This is the start of the #{{ props.toolDetail?.name }} channel. 
      <span>大厅聊天室</span>
    </div>
    <div class="buttonContainer mt-2">
      <button
        type="button"
        class="flex-grow cursor-pointer mr-2 p-[6px] rounded-[4px] w-auto inline h-auto border-0 relative text-3xs font-medium"
      >
        <div class="contents">
          <div
            class="flex justify-start align-center flex-nowrap "
            style="flex: 1 1 auto">
            <div class="buttonIcon mr-[6px] outline-0">
              <font-awesome-icon :icon="['fas', 'pen']" class="text-[var(--text-link)]" />
            </div>
            <div
              class="text-md text-4s font-normal outline-0 text-[var(--text-link)]"
              data-text-variant="text-md/normal">
              Edit Channel
            </div>
          </div>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup>
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faHashtag, faPen } from '@fortawesome/free-solid-svg-icons'
const props = defineProps([
  'tool-detail'
])

</script>

<style lang="scss">
:root {
  --background-accent: hsl(227 calc(1 * 6.5%) 27.3% / 1);
  --header-primary: hsl(220 calc(1 * 13%) 95.5% / 1);
  --header-secondary: hsl( 215 calc( 1 * 8.8%) 73.3% / 1);
  --text-link: hsl( 200 calc( 1 * 100%) 49.4% / 1);
}
</style>

<style lang="scss" scoped>

</style>