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

// Import icon registry
import { iconMap } from '@/components/icons/iconRegistry.js';
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

// iconMap is imported from iconRegistry.js

// Get the icon component based on the name
const iconComponent = computed(() => {
  return iconMap[props.name] || null;
});

// Note: iconMap is available for internal use only


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