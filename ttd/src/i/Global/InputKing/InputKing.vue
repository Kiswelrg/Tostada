<template>
    <div class="inputking flex flex-col px-2 h-fit w-full grow-0 shrink-0 bg-[#313338] z-10">
        <Arg :cur-method-detail="curMethodDetail"
             :cur-args="curArgs"
             v-if="Object.keys(curMethodDetail).length !== 0"
             @update-args="onUpdateArgs"></Arg>
        <div class="wrapper flex justify-between mb-1 w-full h-[44.32px] z-[2] bg-[var(--bg-overlay-3,var(--channeltextarea-background))] rounded-lg">
            <div class="left-buttons h-full flex items-center ml-2">
                <div class="flex">
                    <div class="h-8 w-8 p-1">
                        <!-- display current Bot -->
                        <div class="flex bg-interactive-normal rounded-full justify-center items-center h-6 w-6 text-[#383a40]">
                            <PlusRegular class="h-5 w-5 scale-[0.8] stroke-current"></PlusRegular>
                        </div>
                    </div>
                </div>
            </div>
            <div class="main-input items-center w-full h-full flex mx-2">

                <div class="flex rounded-md shadow-sm w-full h-full text-3s">
                    <div class="flex grow">
                        <input type="text"
                               :placeholder="curPlaceHolder"
                               class="w-full text-md my-2 bg-transparent outline-none font-light"
                               v-model="mainInputText"
                               @keyup.enter="runToolMethod"
                               @paste="pasteContent($event)"
                               >
                        <input class="hidden" ref="chatFiles" type="file" id="chatfiles" name="chatfiles" accept="image/png, image/gif, image/jpeg image/jpg image/webp" multiple>
                    </div>
                </div>

            </div>
            <div class="main-input items-center w-16 flex mx-2">

                <div class="flex shadow-sm w-16 h-8">
                    <div class="h-full">
                        <Drop class="h-8 w-16"
                              :down="false"
                              @on-choose-method="chooseMethod"
                              :cur-method="curMethodCode"
                              :height="30"
                              :menu-gap="6"
                              :has-icon="false"
                              :methods-list="methodsList"></Drop>
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
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import PlusRegular from '@/assets/Server/Channel/InputKing/plus-regular.vue'
import Arg from './Arg/Arg.vue'
import Drop from '../../../components/Util/Drop.vue'
import { computed, ref, onMounted, watch } from 'vue'
import { jsonWithBigInt } from '@/util/parse'
import { getCookie } from '@/util/session'
const props = defineProps([
    'tool-detail',
    'chat-socket'
])

const emit = defineEmits([
    'add-message',
])

onMounted(() => {

})

const mainInputText = ref('')
const chatFiles = ref([])

// Dropup tools
const isRunningTool = ref(false)
const curMethodCode = ref(0)
const curMethod = ref({})
const curArgs = ref({})


const pasteContent = (e) => {
    const items = (e.clipboardData || window.clipboardData).items;
    const files = [];
    for (let item of items) {
        if (item.kind === 'file') {
            files.push(item.getAsFile());
        }
    }

    if (files.length > 0) {
        handleFiles(files);
        e.preventDefault();
    }
}


function getFileType(file) {
    // Get file extension
    const extension = file.name.split('.').pop().toLowerCase();
    
    // Check MIME type
    const mimeType = file.type;

    if (mimeType.startsWith('image/')) {
        return mimeType.split('/')[1]; // Returns 'png', 'jpeg', etc.
    } else if (extension) {
        return extension;
    } else {
        return 'unknown';
    }
}

const handleFiles = (files) => {
    const fileInput = chatFiles.value;
    const dataTransfer = new DataTransfer();

    if (fileInput.files.length >= 10) {
        alert(`You can only upload a maximum of 10 files. now ${fileInput.files.length}`);
        return;
    }
    // Add existing files
    Array.from(fileInput.files).forEach((file) => {
        dataTransfer.items.add(file)
    });

    let cur = dataTransfer.items.length;
    // Add new pasted files
    for (const file of files) {
        if (cur >= 10) {
            break;
        }
        if (!file) return;
        // Check if it's a directory or non-recognizable or empty
        if (file.type === '' || file.size === 0) {
            console.log(`${file.name} is skipped`);
        } else {
            console.log(`${file.name} type : ${getFileType(file)}`);
            dataTransfer.items.add(file);
            cur++;
        }
    }

    if (dataTransfer.files.length > 10) {
        alert(`Error: ${dataTransfer.files.length}`);
        return;
    }
    fileInput.files = dataTransfer.files;
    updateFileCountMessage(fileInput.files.length);
}

const updateFileCountMessage = (fileCount) => {
    // You can update a message in the UI if needed
    console.log(`${fileCount} file(s) selected.`);
}


const onUpdateArgs = (v, k) => {
    curArgs.value[k] = v;
}

// const curMethod = computed(() => {
//     return methodDetail(curMethodCode.value)
// })

const chooseMethod = (m) => {
    if (curMethodCode.value !== m.code) {
        curMethod.value = m
        isRunningTool.value = false
        curMethodCode.value = m.code
    }
}

const curPlaceHolder = computed(() => {
    if (curMethod.value.description === undefined || curMethod.value.description === '')
        return 'Message Here...'
    return curMethod.value.description
})

const methodsList = computed(() => {
    if (props.toolDetail)
        return props.toolDetail['methods']
    return undefined
})

watch(methodsList, (newV) => {
    curArgs.value = {}
    if (newV && newV.groups !== undefined) {
        for (const group of newV.groups) {
            for (const method of group.methods) {
                if (curMethodCode.value != -1) break
                curMethodCode.value = method.code
            }
            if (curMethodCode.value != -1) break
        }
    }
    else
        curMethodCode.value = -1
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
    if (curMethodCode.value == -1) return {}
    return methodDetail(curMethodCode.value)
})

// for now, 
const text2MsgContents = () => {
    let res = []
    res.push({
        'type': 'Text',
        'content': mainInputText.value
    })
    return res
}


function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = error => reject(error);
    });
}


const sendMessageInChannel = async () => {
    if (mainInputText.value === '' && chatFiles.value.files.length === 0) return;

    const d = {
        type: 'normal',
        channel_cid: props.toolDetail.cid.toString(),
        contents: text2MsgContents(),
        is_private: false,
        mentioned_user: undefined,
        tool_used: undefined,
        files: []
    };

    const files = Array.from(chatFiles.value.files);
    for (let file of files) {
        try {
            const fileData = await fileToBase64(file);
            d.files.push({
                name: file.name,
                type: file.type,
                size: file.size,
                data: fileData
            });
        } catch (error) {
            console.error('Error converting file to base64:', error);
            // Handle error appropriately (e.g., show a user-friendly message)
        }
    }

    try {
        props.chatSocket.send(JSON.stringify({ message: d }));
        mainInputText.value = '';
        chatFiles.value.value = null; // Resetting chatFiles to clear the input
        updateFileCountMessage(0); // Reset file count message
    } catch (error) {
        console.error('Error sending message via WebSocket:', error);
        // Handle error appropriately
    }
}

async function runToolMethod() {
    // no tool method
    if (curMethodCode.value == 0 || curMethodCode.value == -1) {
        sendMessageInChannel()
        return
    }
    // forbit running constantly
    if (isRunningTool.value) return
    isRunningTool.value = true

    // set RunTool button available in 5 seconds
    setTimeout(() => {
        isRunningTool.value = false
    }, 5000)

    // set method
    var form_data = new FormData()
    curArgs.value['method-name'] = curMethodDetail.value.display_name
    curArgs.value['method-code'] = curMethodCode.value
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
@import "@/styles/global.scss";
:root {
    --m-inputking-height: 53px;
    --m-inputking-l-indent: 24px;
}
</style>

<style lang="scss" scoped>

</style>