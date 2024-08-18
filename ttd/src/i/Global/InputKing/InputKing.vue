<template>
    <div class="inputking flex flex-col px-2 h-fit w-full grow-0 shrink-0 bg-[#313338] z-10">
        <Arg :cur-method-detail="curMethodDetail"
             :cur-args="curArgs"
             v-if="Object.keys(curMethodDetail).length !== 0"
             @update-args="onUpdateArgs"></Arg>
        <div
             class="wrapper flex justify-between mb-1 w-full h-fit z-[2] bg-[var(--bg-overlay-3,var(--channeltextarea-background))] rounded-lg pl-3">
            <div class="left-buttons w-fit h-full flex items-center m-0">
                <div class="flex self-start">
                    <div class="h-8 w-10 px-2 pt-3">
                        <!-- display current Bot -->
                        <div
                             class="flex bg-interactive-normal rounded-full justify-center items-center h-6 w-6 text-[#383a40]">
                            <PlusRegular class="h-5 w-5 scale-[0.8] stroke-current"></PlusRegular>
                        </div>
                    </div>
                </div>
            </div>
            <div class="main-input items-center w-full h-full flex mx-2">
                <div class="flex rounded-md shadow-sm w-full h-full text-3s">
                    <div class="w-full">
                        <div v-if="inputItems.length === 1 && inputItems[0].length === 1 && inputItems[0][0]['content'] === ''"
                             class="placeholder absolute pt-[11px] whitespace-nowrap text-ellipsis overflow-hidden text-[var(--channel-text-area-placeholder)] select-none pointer-events-none">
                            {{ curPlaceHolder }}</div>
                        <div contenteditable
                             
                             class="markup relative w-full outline-none break-words break-all right-[10px] left-0 whitespace-break-spaces caret-[var(--text-normal)] text-left text-[var(--text-normal))] break py-[11px] pr-[11px] cursor-default"
                             @mousedown.self.prevent
                             @input="inputChange"
                             @keydown="handleKeydown"
                             ref="inputmarkup"
                             >
                             <div v-for="(item, idx1) in inputItems"
                             :key="idx1"
                             @click="clickElement(idx1, $event)"
                             @keydown="console.log(detectSelectionSE())"
                             class="element w-full text-md bg-transparent outline-none font-light select-none cursor-text">
                                <span 
                                      v-for="(it, idx2) in item"
                                      :key="idx2"
                                      :idx1="idx1"
                                      :idx2="idx2"
                                      class="text-[var(--text-normal)] font-medium outline-none select-text"
                                      @paste="pasteContent($event)"
                                      v-html="parseMsgContent(it)"
                                      >
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <div class="upload-files hidden">
                <input class=""
                       ref="chatFiles"
                       type="file"
                       id="chatfiles"
                       name="chatfiles"
                       accept="image/png, image/gif, image/jpeg image/jpg image/webp"
                       multiple>
            </div>

            <div class="main-input items-center w-16 flex mx-2">
                <div class="flex shadow-sm w-16 h-8 self-start">
                    <div class="h-full pt-2">
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
import { computed, ref, onMounted, watch, nextTick } from 'vue'
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

const inputmarkup = ref(undefined)
const mainInputText = ref('')
const inputItems = ref([
    [
        {
            'type': 'text',
            'content': 'asdfg'
        },
        {
            'type': 'text',
            'content': '12345678'
        },
        {
            'type': 'text',
            'content': 'hjkl'
        },
    ],
    [
        {
            'type': 'text',
            'content': ''
        }
    ],
    [
        {
            'type': 'text',
            'content': ''
        }
    ]
])
const chatFiles = ref([])

// Dropup tools
const isRunningTool = ref(false)
const curMethodCode = ref(0)
const curMethod = ref({})
const curArgs = ref({})



const parseMsgContent = (item) => {
    if (item.content == '') return '&#xFEFF;'
    return item.content
}


const removeRange = (list, start, end) => {
    const [startRow, startCol] = start;
    const [endRow, endCol] = end;

    return list.map((row, rowIndex) => {
        if (rowIndex < startRow || rowIndex > endRow) {
            // Rows outside the range remain unchanged
            return row;
        } else if (rowIndex === startRow && rowIndex === endRow) {
            // If start and end are in the same row
            return [...row.slice(0, startCol + 1), ...row.slice(endCol)];
        } else if (rowIndex === startRow) {
            // First row of the range
            return row.slice(0, startCol + 1);
        } else if (rowIndex === endRow) {
            // Last row of the range
            return row.slice(endCol);
        } else {
            // Rows fully within the range are removed
            return [];
        }
    }).filter(row => row.length > 0); // Remove any empty rows
}


const detectSelectionSE = () => {
    const getNodeDetail = (node, offset) => {
        const span = node.nodeType === Node.TEXT_NODE  // this is a must
        ? node.parentElement 
        : node;
        const row = parseInt(span.getAttribute('idx1'), 10)
        const col = parseInt(span.getAttribute('idx2'), 10)
        // const _1th_div = span.parentElement.previousSibling == null || span.parentElement.previousSibling.data == ''
        // const _last_div = span.parentElement.nextSibling == null || span.parentElement.nextSibling.data == ''
        const _1th_div = row == 0
        const _last_div = row == inputItems.value.length - 1
        const _1th_span = col == 0
        console.log(node, span)
        if (isNaN(row)) {return undefined}
        const _last_span = col == inputItems.value[row].length - 1
        const _1th_char = (offset == 0) || (offset == 1 && span.textContent[0] == '\uFEFF')
        const _last_char = (offset == span.textContent.length) || (offset == span.textContent.length - 1 && span.textContent[span.textContent.length - 1] == '\uFEFF')
        let position = 0b000000000
        if (_1th_div) position |= (0b1 << 8)
        if (!_1th_div && !_last_div) position |= (0b1 << 7)
        if (_last_div) position |= (0b1 << 6)
        if (_1th_span) position |= (0b1 << 5)
        if (!_1th_span && !_last_span) position |= (0b1 << 4)
        if (_last_span) position |= (0b1 << 3)
        if (_1th_char) position |= (0b1 << 2)
        if (!_1th_char && !_last_char) position |= (0b1 << 1)
        if (_last_char) position |= (0b1 << 0)
        return {
            'position': position,
            'node': node,
            'offset': offset
        }
    }
    const s = window.getSelection()
    if (!s.rangeCount) return [0, undefined, [undefined, undefined]]
    const r = s.getRangeAt(0)
    const start = r.startContainer
    const end = r.endContainer
    const forward = ((start == end && s.anchorOffset <= s.focusOffset) || (start != end && start == s.anchorNode)) ? true : false
    const _s = getNodeDetail(start, r.startOffset)
    const _e = forward ? getNodeDetail(end, r.endOffset) : _s
    const se = [
        _s, _e
    ]
    return [
        s.rangeCount,
        r.toString(),
        se,
        forward,
    ]
}


const focusInput = (e) => {
    // console.log('T, curT, activeE:', e.target.tagName, e.currentTarget.tagName, document.activeElement)
    const tar = e.target
    const cur = e.currentTarget

}


const inputChange = (e) => {
    const selection = window.getSelection();
    if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const anchorNode = range.startContainer;
        const targetElement = anchorNode.nodeType === Node.TEXT_NODE ? anchorNode.parentElement : anchorNode;

        console.log('Input occurred in:', targetElement.getAttribute('idx1'), targetElement.getAttribute('idx2'));
    }
}


const selectAllSpans = () => {
    window.getSelection().removeAllRanges();
    const range = document.createRange();
    range.setStartBefore(spans.value[0]);
    range.setEndAfter(spans.value[spans.value.length - 1]);
    window.getSelection().addRange(range);
}


const moveCursorToPosition = (element, position) => {
    const range = document.createRange();
    const selection = window.getSelection();
    range.setStart(element.firstChild, position);
    range.collapse(true);
    selection.removeAllRanges();
    selection.addRange(range);
}

function placeCaretAtEnd(el) {
    const range = document.createRange();
    const selection = window.getSelection();
    range.selectNodeContents(el);
    range.collapse(false);  // Move caret to the end
    selection.removeAllRanges();
    selection.addRange(range);
}

const clickElement = (k, e) => {
    // console.log(e.target, e.currentTarget.lastElementChild)
    if (e.target.classList.contains('element')) {
        const range = document.createRange();
        const selection = window.getSelection();
        console.log(e.target.lastElementChild, e.currentTarget == e.target)
        moveCursorToPosition(e.target.lastElementChild, e.target.lastElementChild.textContent.length);
        // range.selectNodeContents(e.target.lastChild);
        // range.collapse(false);
        // selection.removeAllRanges();
        // selection.addRange(range);
    }
}


const handleKeydown = (e) => {
    const se = detectSelectionSE()
    console.log(se)
    if (e.key == 'Backspace') {
        console.log('Backspace')
        if (!se[0]) return
        const start = se[2][0]['node']
        const end = se[2][1]['node']
        const sl = start.nodeType === Node.TEXT_NODE ? start.parentElement : start;
        const el = end.nodeType === Node.TEXT_NODE ? end.parentElement : end
        const [r1, c1] = [sl.getAttribute('idx1'), sl.getAttribute('idx2')]
        const [r2, c2] = [el.getAttribute('idx1'), el.getAttribute('idx2')]
        const xoff = se[2][0]['offset']
        const yoff = se[2][1]['offset']
        console.log(se[2][0]['offset'], se[2][1]['offset'])
        console.log('s == e ?', start === end)
        if (se[1] === '') {
            if (xoff > 0) {
                console.log('r1 c1 xoff:', r1, c1, xoff)
                console.log('trying to delete:', inputItems.value[r1][c1]['content'][xoff - 1])
            } else {
                let cc=c1-1
                while (cc >= 0 && inputItems.value[r1][cc]['content'] === '') {
                    cc--
                    // 最好把这种content==''的去掉在这里
                }
                if (cc === -1) {
                    if (r1 == 0) 
                        console.log('at the very beginning, do nothing')
                    else
                        console.log('trying to merge div, backspace on start of a div, at row:', r1)

                } else {
                    console.log(`trying to delete on the ${c1}th span`)
                }
                
            }
        } else {
            console.log('trying to remove range in:', [r1, c1], [r2, c2])
            // removeRange(inputItems.value, [r1, c1], [r2, c2])
            if (start == end) {
                console.log('trying to delete in 1 span, range:', xoff, yoff)
            } else {
                console.log('trying to delete in 2 span, range:', xoff, yoff)
                if (r1 !== r2 && (inputItems.value[r1].length > c1 + 1 || c2 > 0)) {
                    console.log('trying to merge div(v2)')
                }
            }

        }
        e.preventDefault()
        return
    }
    else if (e.key === 'Enter') {
        if (e.shiftKey) {
            if (!se[0] || se[1] != '') return
            const end = se[2][1]['node']
            console.log(end.nodeType, end)
            const el = end.nodeType === Node.TEXT_NODE ? end.parentElement : end;
            console.log(el.nodeType, el)
            console.log(se)
            const row = parseInt(el.getAttribute('idx1'), 10)
            const col = parseInt(el.getAttribute('idx2'), 10)
            const newLine = [...inputItems.value[row].slice(col)]
            newLine[0].content = end.textContent.slice(se[2][1]['offset'])
            inputItems.value[row].splice(col + 1)
            inputItems.value[row][inputItems.value[row].length - 1] = {
                'type': 'text',
                'content': end.textContent.slice(0, se[2][1]['offset'])
            }
            inputItems.value.splice(row + 1, 0, newLine)
            e.preventDefault()
            nextTick(() => {
                moveCursorToPosition(inputmarkup.value.querySelector(`[idx1="${row+1}"][idx2="0"]`), 0)

            })
            return
        } else {

            if (curMethodCode !== undefined && curMethodCode > 0) {
                runToolMethod()
            }

            // Enter: Send text
            sendMessageInChannel()
            e.preventDefault()
        }
        return
    }
    else if (e.key.startsWith('Arrow')) {
        if (se[0] == 0 || se[2][0] == undefined) {
            e.preventDefault()
            return
        }

        // limit moves out of spans
        const start = se[2][0]
        const pos_s = start['position']
        if (Number(pos_s>>8) === Number(0b1)) {
            if (e.key == 'ArrowUp' || (Number(pos_s&0b000100100)===Number(0b000100100) && e.key == 'ArrowLeft')) {
                e.preventDefault()
                return
            }
        }
        const end = se[2][1]
        const pos_e = end['position']
        if (Number(pos_e&0b001000000) === Number(0b001000000)) {
            if (e.key == 'ArrowDown' || (Number(pos_e&0b000001001)===Number(0b000001001) && e.key == 'ArrowRight')) {
                e.preventDefault()
                return
            }
        }

        // move over invisible \ufeff char
        if (e.key == 'ArrowLeft') {
            console.log(pos_s.toString(2), start['offset'], start['node'].data)
        }

        return
    }

}


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
    return inputItems.value.map(item => item.content).join('\n')
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
    if (inputItems.value.map(item => item.content).join('') === '') {
        console.log('All empty')
    } else {
        // remove all trailing inputitem which has '' content
        while (inputItems.value[inputItems.value.length - 1].content === '') {
            inputItems.value.pop();
        }
    }

    return
    if (mainInputText.value === '' && chatFiles.value.files.length === 0) {
        console.log('Nothing to send!')
        return
    }

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
        // mainInputText.value = '';
        inputItems.value = [];
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

<style lang="scss"
       scoped></style>