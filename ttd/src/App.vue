<script setup>

</script>

<template>
  <div class="main h-full w-full bg-teal-100">
    <!-- <router-link to="/user/">Go to U</router-link> -->
    <router-view></router-view>
  </div>
</template>

<style lang="scss">
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

a.button {
    -webkit-appearance: button;
    -moz-appearance: button;
    appearance: button;
    text-decoration: none;
}

</style>
