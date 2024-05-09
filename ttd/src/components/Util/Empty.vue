<script setup>
import { ref } from 'vue'

defineProps({
  helloText: String,
})

const count = ref(0)
</script>

<template>
  <div class="flex m-auto w-fit gap-4">
    <div v-html="helloText">
    </div>
  </div>
</template>

<style scoped>
a, router-link {
  color: #42b983;
}
</style>
