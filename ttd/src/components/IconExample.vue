<template>
  <div class="icon-example">
    <h2>SVG Icon Examples</h2>
    
    <div class="icon-row">
      <div class="icon-item">
        <SvgIcon icon="icons/example-icon" color="red" :size="32" />
        <span>Red Icon</span>
      </div>
      
      <div class="icon-item">
        <SvgIcon icon="icons/example-icon" color="#3498db" :size="32" />
        <span>Blue Icon</span>
      </div>
      
      <div class="icon-item">
        <SvgIcon icon="icons/example-icon" color="#2ecc71" :size="32" />
        <span>Green Icon</span>
      </div>
      
      <div class="icon-item">
        <SvgIcon icon="icons/example-icon" color="#f39c12" :size="48" />
        <span>Orange Icon (Larger)</span>
      </div>
    </div>
    
    <div class="color-picker">
      <label for="icon-color">Choose a custom color:</label>
      <input 
        type="color" 
        id="icon-color" 
        v-model="customColor" 
        class="color-input"
      />
      
      <div class="icon-item custom">
        <SvgIcon icon="icons/example-icon" :color="customColor" :size="40" />
        <span>Custom Color</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import SvgIcon from './SvgIcon.vue';

const customColor = ref('#9b59b6'); // Default purple color
</script>

<style scoped>
.icon-example {
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  max-width: 600px;
  margin: 0 auto;
}

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

.icon-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
}

.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.color-picker {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}

.color-input {
  width: 50px;
  height: 30px;
  border: none;
  cursor: pointer;
}

.icon-item.custom {
  margin-top: 15px;
}
</style> 