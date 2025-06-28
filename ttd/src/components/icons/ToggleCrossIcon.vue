<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 20 20"
    width="100%"
    height="100%"
  >
    
  <path :fill="fill" d="M5.13231 6.72963L6.7233 5.13864L14.855 13.2704L13.264 14.8614L5.13231 6.72963Z"></path>
  <path :fill="fill" d="M13.2704 5.13864L14.8614 6.72963L6.72963 14.8614L5.13864 13.2704L13.2704 5.13864Z"></path>

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