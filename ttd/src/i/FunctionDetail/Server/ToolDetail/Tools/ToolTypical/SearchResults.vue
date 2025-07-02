<template>
    <div class="search-results flex flex-col h-full w-full bg-[#313338] text-white">
        <!-- Header with result count and filter buttons -->
        <div class="search-header flex items-center justify-between px-4 py-3 border-b border-[#404249]">
            <div class="result-count text-sm text-[#b5bac1]">
                {{ props.searchData.query ? `${resultCount} Results` : 'Search Messages' }}
            </div>
            <div class="filter-buttons flex gap-2">
                <button 
                    @click="setSortOrder('newest')"
                    :class="['px-3 py-1 text-xs rounded transition-colors', 
                             sortOrder === 'newest' ? 'bg-[#5865f2] text-white' : 'bg-[#4e5058] text-[#b5bac1] hover:bg-[#6d7079]']">
                    New
                </button>
                <button 
                    @click="setSortOrder('oldest')"
                    :class="['px-3 py-1 text-xs rounded transition-colors', 
                             sortOrder === 'oldest' ? 'bg-[#5865f2] text-white' : 'bg-[#4e5058] text-[#b5bac1] hover:bg-[#6d7079]']">
                    Old
                </button>
                <button 
                    @click="setSortOrder('relevant')"
                    :class="['px-3 py-1 text-xs rounded transition-colors', 
                             sortOrder === 'relevant' ? 'bg-[#5865f2] text-white' : 'bg-[#4e5058] text-[#b5bac1] hover:bg-[#6d7079]']">
                    Relevant
                </button>
            </div>
        </div>

        <!-- Search results message area -->
        <div class="search-messages flex-1 overflow-y-auto px-4 py-3">
            <div v-if="loading" class="flex items-center justify-center h-32">
                <div class="text-[#b5bac1]">Loading...</div>
            </div>
            <div v-else-if="!searchResults.length && props.searchData.query" class="flex items-center justify-center h-32">
                <div class="text-[#b5bac1]">No results found</div>
            </div>
            <div v-else-if="!searchResults.length && !props.searchData.query" class="flex items-center justify-center h-32">
                <div class="text-[#b5bac1] text-center">
                    <div class="mb-2">🔍</div>
                    <div>Type your search query and press Enter</div>
                </div>
            </div>
            <div v-else class="space-y-4">
                <div 
                    v-for="result in searchResults" 
                    :key="result.id"
                    class="search-result-item p-3 rounded bg-[#2b2d31] hover:bg-[#32353b] transition-colors cursor-pointer"
                    @click="jumpToMessage(result)">
                    <div class="flex items-start gap-3">
                        <img 
                            :src="result.avatar_src || '/static/@me/1F955.svg'" 
                            :alt="result.nickname"
                            class="w-8 h-8 rounded-full flex-shrink-0">
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center gap-2 mb-1">
                                <span class="font-medium text-white">{{ result.nickname }}</span>
                                <span class="text-xs text-[#b5bac1]">{{ formatDate(result.date_sent) }}</span>
                            </div>
                            <div class="text-[#dcddde] text-sm break-words">
                                {{ typeof result.contents === 'string' ? result.contents : result.contents?.content || '' }}
                            </div>
                            <div v-if="result.attachments && result.attachments.length" class="mt-2">
                                <div class="text-xs text-[#b5bac1]">
                                    {{ result.attachments.length }} attachment(s)
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pagination -->
        <div class="search-pagination flex items-center justify-between px-4 py-3 border-t border-[#404249]">
            <button 
                @click="previousPage"
                :disabled="currentPage <= 1"
                :class="['px-3 py-1 text-sm rounded-md transition-colors flex items-center gap-1 bg-transparent border-none',
                         currentPage <= 1 ? 'text-[#6d7079] cursor-not-allowed' : 'text-white hover:bg-[#4e5058]']">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
                </svg>
                Back
            </button>
            
            <div class="flex items-center gap-1">
                <div 
                    v-for="pageNum in visiblePages" 
                    :key="pageNum"
                    @click="goToPage(pageNum)"
                    :class="['px-2 py-1 text-sm rounded-full transition-colors min-w-[28px] cursor-pointer',
                             pageNum === currentPage ? 'bg-[#5865f2] text-white' : 'text-[#b5bac1] hover:bg-[#4e5058]']">
                    <span>{{ pageNum }}</span>
                </div>
                <span v-if="showEllipsis" class="text-[#b5bac1] px-1">...</span>
                <div 
                    v-if="totalPages > 5 && currentPage < totalPages - 2"
                    @click="goToPage(totalPages)"
                    :class="['px-2 py-1 text-sm rounded-full transition-colors min-w-[28px] cursor-pointer',
                             totalPages === currentPage ? 'bg-[#5865f2] text-white' : 'text-[#b5bac1] hover:bg-[#4e5058]']">
                    <span>{{ totalPages }}</span>
                </div>
            </div>

            <button 
                @click="nextPage"
                :disabled="currentPage >= totalPages"
                :class="['px-3 py-1 text-sm rounded-md transition-colors flex items-center gap-1 bg-transparent border-none',
                         currentPage >= totalPages ? 'text-[#6d7079] cursor-not-allowed' : 'text-white hover:bg-[#4e5058]']">
                Next
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z"/>
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
    searchData: {
        type: Object,
        default: () => ({
            query: '',
            results: [],
            totalCount: 0,
            currentPage: 1,
            totalPages: 0
        })
    },
    toolDetail: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['jump-to-message', 'page-change'])

// State
const loading = ref(false)
const sortOrder = ref('newest') // 'newest', 'oldest', 'relevant'

// Computed properties
const searchResults = computed(() => props.searchData.results || [])
const resultCount = computed(() => props.searchData.totalCount || 0)
const currentPage = computed(() => props.searchData.currentPage || 1)
const totalPages = computed(() => props.searchData.totalPages || 0)

const visiblePages = computed(() => {
    const pages = []
    const start = Math.max(1, currentPage.value - 2)
    const end = Math.min(totalPages.value, currentPage.value + 2)
    
    for (let i = start; i <= end; i++) {
        pages.push(i)
    }
    return pages
})

const showEllipsis = computed(() => {
    return totalPages.value > 5 && currentPage.value < totalPages.value - 2
})

// Methods
const setSortOrder = (order) => {
    sortOrder.value = order
    // TODO: Implement actual sorting logic
    console.log('Sort order changed to:', order)
}

const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffTime = Math.abs(now - date)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 1) {
        return 'Yesterday'
    } else if (diffDays < 7) {
        return `${diffDays} days ago`
    } else {
        return date.toLocaleDateString()
    }
}

const jumpToMessage = (result) => {
    emit('jump-to-message', result)
}

const previousPage = () => {
    if (currentPage.value > 1) {
        emit('page-change', currentPage.value - 1)
    }
}

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        emit('page-change', currentPage.value + 1)
    }
}

const goToPage = (pageNum) => {
    emit('page-change', pageNum)
}

// Watch for search data changes to update loading state
watch(() => props.searchData, (newData) => {
    if (newData && newData.query && newData.results.length === 0) {
        loading.value = true
        setTimeout(() => {
            loading.value = false
        }, 300)
    } else {
        loading.value = false
    }
}, { deep: true })
</script>

<style lang="scss" scoped>
.search-messages {
    &::-webkit-scrollbar {
        background-color: transparent;
        width: 12px;
        height: 100%;
    }

    &::-webkit-scrollbar-thumb {
        background-color: rgb(27, 27, 27);
        border: 2px solid rgba(0, 0, 0, 0);
        background-clip: padding-box;
        border-radius: 5px;
    }
}

.search-result-item {
    transition: all 0.15s ease;
}
</style>