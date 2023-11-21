<script setup>

</script>

<template>
  <div class="main flex flex-row grow h-full w-full">
    <div class="serverlist flex"></div>
    <div class="server flex flex-row w-full">
      <div class="toollist flex flex-auto bg-orange-100"></div>
      <div class="tooldetail flex grow basis-full bg-orange-50 w-full"></div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.main {
  height: 100%;
  .serverlist {
    background-color: #1e1f22;
    width: 72px;
  }

  .server {
    .toollist {
      background-color: #2b2d31;
      width: 240px;
    }

    .tooldetail {
      background-color: #313338;
    }
  }
}


</style>
