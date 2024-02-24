<template>

  <div class="tooldetail bg-tooldetail-bg flex grow bg-orange-50 w-full">
      <!-- Component changes when currentTab changes -->
      <component :is="tabs['currentTab']"></component>
  </div>

</template>

<script setup>
import { ref, shallowRef } from 'vue'
import PlaygroundTypical from './PlaygroundTypical/PlaygroundTypical.vue'
const tabs = shallowRef({
  'currentTab': PlaygroundTypical,

})

</script>

<style lang="scss" scoped>

</style>