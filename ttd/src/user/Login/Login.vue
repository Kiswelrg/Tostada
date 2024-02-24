<template>
<div class="flex w-full h-full justify-center">
    <UserSignInVue></UserSignInVue>

</div>
</template>

<script setup>
import { onMounted } from 'vue'
import UserSignInVue from '../../components/User/UserSignIn.vue'


onMounted(() => {
    console.log(import.meta.env.VITE_BACKEND_URL)

})
</script>

<style lang="scss" scoped>

</style>