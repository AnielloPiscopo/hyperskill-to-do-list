<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
</script>

<template>
    <header>
        <nav v-if="authStore.isAuthenticated">
            <RouterLink :to="{ name: 'boards' }">Board</RouterLink>
            <RouterLink :to="{ name: 'trash' }">Cestino</RouterLink>
            <RouterLink :to="{ name: 'profile' }">Profilo</RouterLink>
            <button @click="authStore.logout()">Logout</button>
        </nav>
    </header>
</template>