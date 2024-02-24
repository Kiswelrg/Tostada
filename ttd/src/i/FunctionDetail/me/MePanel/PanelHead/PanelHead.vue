<template>
  <div class="serverhead w-full h-12">

    <div class="wrapper m-0 w-full h-full">
      <div class="flex flex-row px-4 py-3 w-full">
        <button class="h-[28px] w-full overflow-hidden rounded bg-[#1e1f22] text-[#949ba4] text-left text-3s whitespace-nowrap outline-none border-0 px-1.5 py-0">
          Find a server
        </button>

        <!-- someting else-->
        <div class="some thing else"></div>
      </div>
    </div>

    <!-- someting else-->
    <div class="wrapper"></div>
  </div>
</template>
  
<script setup>
import { ref } from 'vue'
const thumb_url = '/static/tool/main/thumb.svg'


</script>
  
<style lang="scss" scoped>
.serverhead {
  box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.5);
}

.dropdownarror {

  &::before,
  &::after {
    content: "";
    position: absolute;
    width: 2px;
    /* Adjust the width of the pillars */
    height: 8px;
    background-color: white;
    /* Adjust the color of the pillars */
    top: 50%;
    border-radius: 3px;
  }

  &::before {
    right: 22%;
    transform: rotate(-45deg);
  }

  &::after {
    right: 0;
    transform: rotate(45deg);
  }
}</style>