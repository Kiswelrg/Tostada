<template>
    <div class="inputking flex flex-col px-2 h-fit w-full grow-0 shrink-0 bg-[#313338] z-10">
        <Arg :cur-method-detail="curMethodDetail" :cur-args="curArgs" v-if="Object.keys(curMethodDetail).length !== 0" @update-args="onUpdateArgs"></Arg>
        <div class="wrapper flex justify-between mb-1 bg-[#383a40] w-full h-[44.32px] rounded-lg z-[2]">
            <div class="left-buttons h-full flex items-center ml-2">
                <div class="flex">
                    <div class="h-8 w-8 bg-[#2f2f2f] rounded-full">

                    </div>
                </div>
            </div>
            <div class="main-input items-center w-full h-full flex mx-2">

                <div class="flex rounded-md shadow-sm w-full h-full">
                    <div class="flex">
                        <input type="text" placeholder="Message here" class="w-full text-md my-2 bg-inputking-bg outline-none font-light"
                        @keyup.enter="runToolMethod">
                    </div>
                </div>

            </div>
            <div class="main-input items-center w-16 flex mx-2">

                <div class="flex shadow-sm w-16 h-8">
                    <!-- <input type="submit" class="border-[1px] w-full h-8 rounded-md text-[12px] my-auto bg-[#2f3135] hover:bg-[#4f5258] outline-none font-light"> -->
                    <div class="h-full">
                        <Drop class="h-8 w-16" :down="false" 
                        @on-choose-method="chooseMethod"
                        :cur-method="curMethod"
                        :height="30" :menu-gap="6" :has-icon="false" :methods-list="methodsList"></Drop>
                    </div>
                </div>

            </div>
            <div class="hidden flex right-buttons h-full items-center mr-2">
                <div>
                    <div class="mx-1 h-8 w-8 bg-[#2f2f2f] rounded-lg"></div>
                </div>
                <div>
                    <div class="mx-1 h-8 w-8 bg-[#2f2f2f] rounded-lg"></div>
                </div>
                <div>
                    <div class="mx-1 h-8 w-8 bg-[#2f2f2f] rounded-lg"></div>
                </div>
            </div>
        </div>
        <div class="h-[3px] w-full bg-white rounded-lg"></div>
        
    </div>
</template>

<script setup>
import Arg from './Arg/Arg.vue'
import Drop from '../../../components/Util/Drop.vue'
import { computed, ref, onMounted, watch } from 'vue';
import { jsonWithBigInt } from '@/util/parse'
import { getCookie } from '@/util/session'
const props = defineProps([
    'tool-detail',
])

const emit = defineEmits([
    'add-message',
    
])

onMounted(() => {
    
})


const isDropMenuOpen = ref(false)
const isRunningTool = ref(false)

const curMethod = ref(-1)
const curArgs = ref({})

const onUpdateArgs = (v, k) => {
    curArgs.value[k] = v;
}

const chooseMethod = (code) => {
    if (curMethod.value !== code) {
        isRunningTool.value = false
        curMethod.value = code
    }
}

const methodsList = computed(() => {
    if (props.toolDetail)
        return props.toolDetail['methods']
    return undefined
})

watch(methodsList, (newV) => {
    curArgs.value = {}
    if (newV)
        for (const group of newV.groups) {
            for (const method of group.methods) {
                if (curMethod.value != -1) break
                curMethod.value = method.code
            }
            if (curMethod.value != -1) break
        }
    else
        curMethod.value = -1
})

const methodDetail = (c) => {
    if (!methodsList.value) return {}
    for (const group of methodsList.value.groups) {
        for (const method of group.methods) {
            if (method?.code == c) {
                return method
            }
        }
    }
    return {}
}

const curMethodDetail = computed(() => {
    if (curMethod.value == -1) return {}
    return methodDetail(curMethod.value)
})

async function runToolMethod() {
  console.log('running tool method...')
  if (isRunningTool.value) return
  isRunningTool.value = true
  var form_data = new FormData()
  curArgs.value['method-name'] = curMethodDetail.value.display_name
  curArgs.value['method-code'] = curMethod.value
  curArgs.value['sub_class'] = props.toolDetail['additional']['sub_class']

  for (var v in curArgs.value) {
    form_data.append(v, curArgs.value[v])
  }
  const response = await fetch(
    `/api/i/runtool/${props.toolDetail.cid}/`,
    {
      method: "POST",
      body: form_data,
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      }
    }
  )
  if (response.ok) {
    const text = await response.text()
    const r = jsonWithBigInt(text)
    console.log(`RunTool (fetch status: ${r.r}): `)
    const d = JSON.parse(r.data)
    emit('add-message', d)

  } else {
    console.log(response.status)
  }
  isRunningTool.value = false
}


</script>


<style lang="scss">
:root {
    --m-inputking-height: 53px;
    --m-inputking-l-idt: 24px;
}
</style>
<style lang="scss" scoped></style>