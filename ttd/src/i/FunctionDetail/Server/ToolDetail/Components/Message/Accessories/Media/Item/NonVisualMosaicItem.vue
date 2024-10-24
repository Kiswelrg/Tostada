<template>
  <div class="nonVisualMediaItem mt-2 w-fit max-w-full group/nonvisualmediaitem">
    <div class="MosaicItem relative rounded-sm w-full items-center flex flex-row flex-nowrap max-w-full h-full">
      <div class="attachment p-4 rounded-lg w-[432px] max-w-full flex-auto bg-[var(--background-secondary)] border-[color:var(--background-secondary-alt)] items-center flex-row flex box-border tracking-normal border border-solid border-transparent">
        <img :src="MosiacItemIcon" alt="" class="-indent-[9999px] w-[30px] h-[40px] mr-2 flex-shrink-0" />
        <div class="attachmentInner grow shrink basis-0 whitespace-nowrap text-ellipsis overflow-hidden">
          <div class="filename text-[color:var(--text-link)] whitespace-nowrap text-ellipsis overflow-hidden"><a :href="'/api' + props.item.url" class="anchor text-[color:var(--text-link)] decoration-[color:var(--link-decoration)] cursor-pointer">{{ props.item.name }}</a></div>
          <div class="metadata leading-4 text-xs font-normal text-[color:var(--primary-400)] mr-2">{{ formatFileSize(props.item.size) }}</div>
        </div>
      </div>

      <div class="hoverButtonGroup -top-2 -right-2 outline-[2px] outline outline-[var(--background-secondary)] flex opacity-0 z-[2] absolute rounded-[5px] bg-[color:var(--background-primary)] overflow-hidden group-hover/nonvisualmediaitem:opacity-100">
        <a :href="'/api' + props.item.url" class="anchorOnHover flex p-[8px] text-[color:var(--interactive-normal)] cursor-pointer hover:bg-[var(--background-modifier-hover)] hover:text-[var(--white)]">
          <font-awesome-icon
            :icon="['fas', 'download']"
            class="block h-4 w-4 object-contain"
        /></a>
        <div class="hoverButtonRemove flex p-[8px] text-[color:var(--interactive-normal)] cursor-normal hover:bg-[var(--menu-item-danger-active-bg)] hover:text-[var(--white)]">
          <font-awesome-icon
            :icon="['fas', 'trash']"
            class="block h-4 w-4 object-contain"
            @click="deleteAttachment"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { jsonWithBigInt } from '@/util/parse'
import { getCookie } from '@/util/session'

const props = defineProps(["item"])

const MosiacItemIcon = ref("/static/Message/Attachment/MosaicItem.svg")


const formatFileSize = (bytes) => {
    const sizes = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'RB', 'QB'];
    if (bytes === 0) return '0 bytes';
    const i = Math.floor(Math.log(bytes) / Math.log(1000));
    return parseFloat((bytes / Math.pow(1000, i)).toFixed(2)) + ' ' + sizes[i];
}


const attachmentCID = computed(() => {
  const match = props.item.url.match(/\/(\d+)\/(\d+)\//);

  if (match) {
    const extractedValue = match[2];
    return extractedValue;
  } else {
    return '';
  }
})


const deleteAttachment = async () => {
  const currentCID = attachmentCID.value;
  if (currentCID == '') {
    console.log('Not a valid attachment');
    return;
  }
  const response = await fetch(
      `/api/attachment/deletemsgatm/${currentCID}/`,
      {
          method: "POST",
          headers: {
              "X-CSRFToken": getCookie("csrftoken")
          }
      }
  )
  if (response.ok) {
      const text = await response.text()
      const r = jsonWithBigInt(text)
      console.log(`Delete ATM (fetch status: ${r.r}): ${r.message}`)
      // delete message rendering...

  } else {
      console.log(response.status)
  }
}


</script>

<style lang="scss" scoped></style>
