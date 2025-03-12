<template>
  <div class="p-4">
    <h2 class="text-xl mb-4">Icon Coloring Examples</h2>
    
    <div class="grid grid-cols-3 gap-4">
      <!-- Direct color example -->
      <div class="p-2 border rounded">
        <h3 class="mb-2">Direct Color</h3>
        <IconSystem 
          name="invite"
          color="blue"
          :size="24"
        />
      </div>
      
      <!-- Tailwind color class example -->
      <div class="p-2 border rounded">
        <h3 class="mb-2">Tailwind Class</h3>
        <IconSystem 
          name="invite"
          colorClass="text-interactive-normal"
          :size="24"
        />
      </div>
      
      <!-- Inherited color example -->
      <div class="p-2 border rounded text-red-500">
        <h3 class="mb-2">Inherited Color</h3>
        <IconSystem 
          name="invite"
          :size="24"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import IconSystem from '@/components/IconSystem.vue';
</script> 