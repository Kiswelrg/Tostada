<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 20 20"
    width="100%"
    height="100%"
  >
    
  <path :fill="fill" d="M7.89561 14.8538L6.30462 13.2629L14.3099 5.25755L15.9009 6.84854L7.89561 14.8538Z"></path>
  <path :fill="fill" d="M4.08643 11.0903L5.67742 9.49929L9.4485 13.2704L7.85751 14.8614L4.08643 11.0903Z"></path>

  </svg>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  color: {
    type: String,
    default: 'currentColor'
  }
});

const inheritedColor = ref('currentColor');

// The fill color is either the explicitly provided color prop
// or the inherited color from the parent element
const fill = computed(() => {
  return props.color !== 'currentColor' ? props.color : inheritedColor.value;
});

</script>