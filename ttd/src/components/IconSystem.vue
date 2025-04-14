<template>
  <div 
    ref="wrapper"
    class="icon-wrapper" 
    :class="colorClass" 
    :style="{ width: size + 'px', height: size + 'px' }"
  >
    <component 
      v-if="iconComponent" 
      :is="iconComponent" 
      :color="props.colorClass ? undefined : props.color"
      class="icon-content"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Import all icon components directly
import PlusIcon from '@/components/icons/PlusIcon.vue';
import CircleIcon from '@/components/icons/CircleIcon.vue';
// Add more icons as needed
import InviteIcon from '@/components/icons/InviteIcon.vue';
import SearchIcon from '@/components/icons/SearchIcon.vue';
import CloseIcon from '@/components/icons/CloseIcon.vue';
import ChevronDownIcon from '@/components/icons/ChevronDownIcon.vue';
const wrapper = ref(null);

const props = defineProps({
  // Name of the icon to display
  name: {
    type: String,
    required: true
  },
  // Color of the icon (direct color value)
  color: {
    type: String,
    default: 'currentColor'
  },
  // Tailwind CSS class for coloring (takes precedence over color prop)
  colorClass: {
    type: String,
    default: ''
  },
  // Size of the icon in pixels
  size: {
    type: Number,
    default: 24
  }
});

// Map of icon names to components
const iconMap = {
  'plus': PlusIcon,
  'circle': CircleIcon,
  'invite': InviteIcon,
  'search': SearchIcon,
  'close': CloseIcon,
  'chevron-down': ChevronDownIcon
  // Add more mappings as needed
};

// Get the icon component based on the name
const iconComponent = computed(() => {
  return iconMap[props.name] || null;
});


</script>

<style scoped>
.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.icon-content {
  width: 100%;
  height: 100%;
}
</style> 