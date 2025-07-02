<template>
<div class="toolbar flex m-0 h-8 items-center justify-between">
    <div class="flex items-center gap-2">
        <div class="wrapper h-full w-8 flex items-center justify-center cursor-pointer transition-colors">
            <IconSystem 
              name="map-pin"
              colorClass="text-interactive-normal"
              :size="20"
            />
        </div>
        <div class="wrapper h-full w-8 flex items-center justify-center cursor-pointer transition-colors">
            <IconSystem 
              name="member-list"
              colorClass="text-interactive-normal"
              :size="20"
            />
        </div>
    </div>
    
    <div class="flex-1 mx-4 w-[244px]">
        <div class="relative">
            <div class="bg-[#28292d] rounded h-7 flex items-center px-2">
                <div class="flex-1 relative" @click="focusSearch">
                    <div v-if="!searchValue" class="absolute left-0 top-0 bottom-0 flex items-center text-text-muted pointer-events-none text-sm">
                        Search
                    </div>
                    <div 
                        class="min-h-[16px] outline-none text-text-normal cursor-text text-sm leading-none w-full text-left whitespace-nowrap overflow-hidden"
                        contenteditable="true"
                        @input="onSearchInput"
                        @keydown="onKeyDown"
                        @paste="onPaste"
                        @focus="onSearchFocus"
                        @blur="onSearchBlur"
                        ref="searchInput"
                    ></div>
                </div>
                <div class="ml-1 flex-shrink-0">
                    <IconSystem 
                        v-if="!searchValue"
                        name="search"
                        colorClass="text-text-muted"
                        :size="14"
                    />
                    <IconSystem 
                        v-else
                        name="close"
                        colorClass="text-text-muted hover:text-text-normal cursor-pointer"
                        :size="14"
                        @click="clearSearch"
                    />
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import { ref, watch, inject } from 'vue'
import IconSystem from '@/components/IconSystem.vue'

const props = defineProps({
  toolDetail: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['search-results', 'search-cleared', 'search-focused'])

const searchValue = ref('')
const searchFocused = ref(false)
const searchInput = ref(null)
const isSearching = ref(false)
const searchTimeout = ref(null)

const onSearchInput = (event) => {
  // Remove any line breaks and keep only single line text
  const text = event.target.textContent.replace(/\n/g, ' ').trim()
  searchValue.value = text
  
  // Update the input content to ensure no line breaks
  if (event.target.textContent !== text) {
    event.target.textContent = text
    // Move cursor to end
    const range = document.createRange()
    const selection = window.getSelection()
    range.selectNodeContents(event.target)
    range.collapse(false)
    selection.removeAllRanges()
    selection.addRange(range)
  }
}

const onKeyDown = (event) => {
  // Prevent Enter from creating new lines
  if (event.key === 'Enter') {
    event.preventDefault()
    // Trigger immediate search on Enter
    if (searchValue.value.trim()) {
      // Clear existing timeout
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value)
      }
      performSearch(searchValue.value.trim())
    }
  }
}

const onPaste = (event) => {
  event.preventDefault()
  // Get pasted text and remove line breaks
  const paste = event.clipboardData?.getData('text') || ''
  const cleanText = paste.replace(/\n/g, ' ').trim()
  
  // Insert the clean text using modern approach
  const selection = window.getSelection()
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0)
    range.deleteContents()
    range.insertNode(document.createTextNode(cleanText))
    range.collapse(false)
    
    // Trigger input event manually to update searchValue
    const inputEvent = new Event('input', { bubbles: true })
    event.target.dispatchEvent(inputEvent)
  }
}

const clearSearch = () => {
  searchValue.value = ''
  if (searchInput.value) {
    searchInput.value.textContent = ''
    searchInput.value.focus()
  }
  emit('search-cleared')
}

const onSearchFocus = () => {
  searchFocused.value = true
  // Emit focus event to show search area with previous results if any
  emit('search-focused')
}

const onSearchBlur = (event) => {
  if (searchInput.value && searchInput.value.textContent.trim() !== '') {
    // If still searching, don't clear focus
    return
  }

  // Check if focus is moving to an element within the search results area
  if (event.relatedTarget && event.relatedTarget.closest('.search-results')) {
    return // Don't close search if clicking within search results
  }
  
  searchFocused.value = false
}

const focusSearch = () => {
  if (searchInput.value) {
    searchInput.value.focus()
  }
}

const performSearch = async (query, page = 1) => {
  if (!query.trim()) {
    emit('search-cleared')
    return
  }

  isSearching.value = true
  
  try {
    const response = await fetch(`/api/messages/search/?q=${encodeURIComponent(query)}&page=${page}&channel_id=${(props.toolDetail?.cid).toString()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      emit('search-results', {
        query: query,
        results: data.results || [],
        totalCount: data.count || 0,
        currentPage: page,
        totalPages: Math.ceil((data.count || 0) / 25)
      })
    } else {
      console.error('Search failed:', response.status)
      emit('search-results', {
        query: query,
        results: [],
        totalCount: 0,
        currentPage: 1,
        totalPages: 0
      })
    }
  } catch (error) {
    console.error('Search error:', error)
    emit('search-results', {
      query: query,
      results: [],
      totalCount: 0,
      currentPage: 1,
      totalPages: 0
    })
  } finally {
    isSearching.value = false
  }
}

// Watch for focus changes to handle search clearing when focus is lost
watch(searchFocused, (focused) => {
  if (!focused) {
    // Clear search when losing focus regardless of search value
    emit('search-cleared')
  }
})

// Expose performSearch for pagination
defineExpose({
  performSearch
})

</script>

<style lang="scss" scoped>

</style>