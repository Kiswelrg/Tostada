<script setup>

</script>

<template>
  <div class="main flex flex-row grow h-full w-full">
    <div class="serverlist flex bg-gray-950"></div>
    <div class="server flex flex-row w-full">
      <div class="toollist flex flex-auto bg-gray-800"></div>
      <div class="tooldetail flex grow basis-full bg-gray-400 w-full"></div>
    </div>
  </div>
</template>

<style scoped>
.main {
  height: 100%;
}
.serverlist {
  width: 72px;
}

.toollist {
  width: 240px;
}

</style>
