<script setup>
import { ref } from 'vue'

defineProps({
  
})

const count = ref(0)
</script>

<template>
  <div class="flex m-auto w-fit gap-4">
      <a href="/">Home</a>
      <a href="/i/">Tool</a>
      <a href="/a/">User</a>
      <a href="/blablabla/">..</a>
  </div>
</template>

<style scoped>
a, router-link {
  color: #42b983;
}
</style>
