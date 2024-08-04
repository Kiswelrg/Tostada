<template>
    <div class="absolute h-screen w-screen pointer-events-none">
        <Popups v-if="showMsgMenu"
                ref="popup"
                v-click-outside="[closePopup, msgMenuTrigger]"
                :cid="curMsgCid"
                :popup-type="popupType"
                :style="popupPosition"></Popups>
    </div>
</template>

<script setup>
import Popups from './Popup/Popups.vue'
import { computed, ref, nextTick } from 'vue'

const popup = ref(null)

const showMsgMenu = ref(false)

const menuList = ref([
    showMsgMenu
])

const msgMenuTrigger = ref(undefined)
const curMsgCid = ref(-1)

const popupTypes = ref([
    'MsgMenu'
])

const popupIndex = ref(0)

const popupType = computed(() => {
    return popupTypes.value[popupIndex.value]
})

const popupPosition = ref({
    'right': 0,
    'top': 0,
    'max-height': 'fit-content'
})

const open = async (action, target, cid) => {
    const coords = target.getBoundingClientRect()
    if (msgMenuTrigger.value !== undefined) {
        if (target !== msgMenuTrigger.value) {
            showMsgMenu.value = false
            msgMenuTrigger.value = undefined
        } else {
            showMsgMenu.value = false
            msgMenuTrigger.value = undefined
            return
        }
    }
    msgMenuTrigger.value = target
    showMsgMenu.value = true
    curMsgCid.value = cid
    await nextTick()
    const itemW = popup.value.$el.offsetWidth
    const itemH = popup.value.$el.offsetHeight
    if (action === 'MsgMenu') {
        // coords being the bounding rect of the triggering button(ellipse)
        const h = document.documentElement.clientHeight || window.innerHeight || 0
        const w = document.documentElement.clientWidth || window.innerWidth || 0
        if (h <= itemH + 20 || w <= itemW + 20) {
            console.log('not enough space')
            popupPosition.value = {
                'right': (w - coords.left + 7).toString() + 'px',
                'bottom': '20px',
                'max-height': (h - 20).toString() + 'px',
            }
        } else if (coords.top + itemH + 20 > h) {
            popupPosition.value = {
                'right': (w - coords.left + 7).toString() + 'px',
                'bottom': '20px',
                'max-height': 'fit-content',
            }
        } else {
            popupPosition.value = {
                'right': (w - coords.left + 7).toString() + 'px',
                'bottom': (h - coords.top - itemH).toString() + 'px',
                'max-height': 'fit-content',
            }
        }
        
    }
}

const closePopup = () => {
    showMsgMenu.value = false
    msgMenuTrigger.value = undefined
}

defineExpose({
  open
});


</script>

<style lang="scss" scoped>

</style>