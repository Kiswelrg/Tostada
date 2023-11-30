<template>
    <div class="main h-full w-full flex flex-col bg-white">
        <Header />
        <!-- Component changes when currentTab changes -->
        <a href="/user/">Home</a> |
        <a href="/user/login/">Login</a> |
        <a href="/user/signup/">Sign Up</a>
        <div @click="show" class="cursor-pointer">111</div>
        <component :is="tabs['currentTab']"></component>
    </div>
</template>

<script setup>
import Header from './Header/Header.vue'
import { ref, computed } from 'vue'
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

<style lang="scss" setup>

</style>