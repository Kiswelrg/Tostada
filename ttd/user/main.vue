<template>
    <div class="main h-full w-full flex flex-col bg-white">
        <Header />
        <!-- Component changes when currentTab changes -->
        <component :is="tabs['currentTab']"></component>
    </div>
</template>

<script setup>
import Header from './Header/Header.vue'
import { ref } from 'vue'
import Home from './Home/Home.vue'
import Login from './Login/Login.vue'
import Signup from './Signup/Signup.vue'

const tabs = ref({
    currentTab: Home,
    all: [
        'Home',
        'Login',
        'Signup',
        'About',
        'Contact',
    ]
})

</script>

<style lang="scss" setup></style>