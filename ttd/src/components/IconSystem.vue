<template>
  <div class="icon-wrapper" :style="{ width: size + 'px', height: size + 'px' }">
    <component 
      v-if="iconComponent" 
      :is="iconComponent" 
      :color="color" 
      class="icon-content"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// Import all icon components directly
import PlusIcon from '@/components/icons/PlusIcon.vue';
import CircleIcon from '@/components/icons/CircleIcon.vue';
import InviteIcon from '@/components/icons/InviteIcon.vue';
// Add more icons as needed

const props = defineProps({
  // Name of the icon to display
  name: {
    type: String,
    required: true
  },
  // Color of the icon
  color: {
    type: String,
    default: 'currentColor'
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
  'invite': InviteIcon
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