<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 24 24"
    width="100%"
    height="100%"
  >
    <path 
      :fill="color" 
      d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"
    />
  </svg>
</template>

<script setup>
defineProps({
  color: {
    type: String,
    default: 'currentColor'
  }
});
</script> 