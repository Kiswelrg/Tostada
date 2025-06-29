<template>
  <div class="p-8 max-w-6xl mx-auto h-full overflow-auto">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2 text-gray-800 dark:text-white">Icon Gallery</h1>
      <p class="text-gray-600 dark:text-gray-400 mb-6">Available icons in the IconSystem</p>
      
      <div class="flex gap-4 items-center flex-wrap">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search icons..." 
          class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded text-base min-w-[200px] bg-white dark:bg-gray-700 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        
        <div class="flex items-center gap-2">
          <label class="text-gray-700 dark:text-gray-300">Size:</label>
          <select 
            v-model="iconSize" 
            class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option :value="16">16px</option>
            <option :value="24">24px</option>
            <option :value="32">32px</option>
            <option :value="48">48px</option>
            <option :value="64">64px</option>
          </select>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-8">
      <div 
        v-for="iconName in filteredIcons" 
        :key="iconName"
        class="border border-gray-200 dark:border-gray-600 rounded-lg p-6 text-center cursor-pointer transition-all duration-200 bg-white dark:bg-gray-800 hover:border-blue-500 hover:shadow-lg hover:-translate-y-0.5 hover:bg-gray-50 dark:hover:bg-gray-700"
        @click="copyIconName(iconName)"
        :title="`Click to copy: ${iconName}`"
      >
        <div class="mb-4 flex justify-center items-center min-h-[64px]">
          <IconSystem 
            :name="iconName" 
            :size="iconSize"
            color="#666"
          />
        </div>
        <div class="font-semibold mb-2 text-gray-800 dark:text-gray-200 text-sm">{{ iconName }}</div>
        <div class="font-mono text-xs text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded break-all">
          &lt;IconSystem name="{{ iconName }}" /&gt;
        </div>
      </div>
    </div>

    <div v-if="filteredIcons.length === 0" class="text-center text-gray-600 dark:text-gray-400 italic mt-12">
      No icons found matching "{{ searchQuery }}"
    </div>

    <!-- Copy notification with custom animation -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="translate-x-full opacity-0"
      enter-to-class="translate-x-0 opacity-100"
      leave-active-class="transition-all duration-300 ease-in"
      leave-from-class="translate-x-0 opacity-100"
      leave-to-class="translate-x-full opacity-0"
    >
      <div v-if="showCopyNotification" class="fixed bottom-8 right-8 bg-green-600 text-white px-4 py-3 rounded shadow-lg z-50">
        Copied "{{ lastCopiedIcon }}" to clipboard!
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import IconSystem from '@/components/IconSystem.vue';
import { getAvailableIcons } from '@/components/icons/iconRegistry.js';

// Dynamically get all available icons from the icon registry
const availableIcons = getAvailableIcons();

const searchQuery = ref('');
const iconSize = ref(32);
const showCopyNotification = ref(false);
const lastCopiedIcon = ref('');

const filteredIcons = computed(() => {
  if (!searchQuery.value) {
    return availableIcons;
  }
  return availableIcons.filter(icon => 
    icon.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const copyIconName = async (iconName) => {
  try {
    await navigator.clipboard.writeText(iconName);
    lastCopiedIcon.value = iconName;
    showCopyNotification.value = true;
    
    // Hide notification after 2 seconds
    setTimeout(() => {
      showCopyNotification.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy to clipboard:', err);
  }
};

onMounted(() => {
  console.log(`IconGallery loaded with ${availableIcons.length} icons`);
});
</script>