<script setup>
import { RouterLink, RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue'
</script>

<template>
    <div>
        <Navbar />
        <div>
            <RouterView />
        </div>
    </div>
</template>
  