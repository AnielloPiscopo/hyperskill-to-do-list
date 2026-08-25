<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
</script>

<template>
    <header>
        <nav v-if="authStore.isAuthenticated" class="navbar navbar-expand-sm border-bottom"
            style="border-color: var(--paper-border) !important;">
            <div class="container">
                <RouterLink :to="{ name: 'boards' }" class="navbar-brand">Tasky</RouterLink>
                <div class="d-flex gap-2 align-items-center">
                    <RouterLink :to="{ name: 'boards' }" class="btn btn-sm btn-outline-secondary rounded-pill">Boards
                    </RouterLink>
                    <RouterLink :to="{ name: 'trash' }" class="btn btn-sm btn-outline-secondary rounded-pill">Trash
                    </RouterLink>
                    <RouterLink :to="{ name: 'profile' }" class="btn btn-sm btn-outline-secondary rounded-pill">Profile
                    </RouterLink>
                    <button class="btn btn-sm btn-primary rounded-pill" @click="authStore.logout()">Logout</button>
                </div>
            </div>
        </nav>
    </header>
</template>