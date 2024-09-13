<script setup>
import { ref } from 'vue'

defineProps({
  helloText: String,
})

const count = ref(0)
</script>

<template>
  <div class="flex flex-col m-auto w-fit gap-4">
    <div v-html="helloText">
    </div>
    <div class="border-2 rounded border-solid w-fit self-center px-2">Site by Kiswelrg</div>
  </div>
</template>

<style scoped>
a, router-link {
  color: #42b983;
}
</style>
