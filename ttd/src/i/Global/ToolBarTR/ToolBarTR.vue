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
                <div class="flex-1 relative">
                    <div v-if="!searchValue" class="absolute inset-0 flex items-center text-text-muted pointer-events-none text-sm">
                        Search
                    </div>
                    <div 
                        class="min-h-[16px] outline-none text-text-normal cursor-text text-sm leading-none"
                        contenteditable="true"
                        @input="onSearchInput"
                        @focus="searchFocused = true"
                        @blur="searchFocused = false"
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
import { ref } from 'vue'
import IconSystem from '@/components/IconSystem.vue'

const searchValue = ref('')
const searchFocused = ref(false)
const searchInput = ref(null)

const onSearchInput = (event) => {
  searchValue.value = event.target.textContent
}

const clearSearch = () => {
  searchValue.value = ''
  if (searchInput.value) {
    searchInput.value.textContent = ''
    searchInput.value.focus()
  }
}

</script>

<style lang="scss" scoped>

</style>