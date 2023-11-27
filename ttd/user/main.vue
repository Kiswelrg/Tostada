<template>
    <div class="main h-full w-full flex flex-col bg-white">
        <Header />
        <!-- Component changes when currentTab changes -->
        <component :is="tabs[currentTab]"></component>
    </div>
</template>

<script setup>
import Header from './Header/Header.vue'
import { ref } from 'vue'
const tabs = ref({
    currentTab: 'Home',
    all: [
        'Home',
        'About',
        'Contact',
        'Login',
        'Signup'
    ]
})

</script>

<style lang="scss" setup></style>