<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
</script>

<template>
    <header class="border-bottom mb-3">
        <nav v-if="authStore.isAuthenticated" class="navbar navbar-expand-sm border-bottom"
            style="border-color: var(--paper-border) !important;">
            <div class="container">
                <RouterLink :to="{ name: 'boards' }" class="navbar-brand my-navbar-brand">Tasky</RouterLink>

                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav"
                    aria-controls="mainNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div id="mainNav" class="collapse navbar-collapse">
                    <div class="d-flex flex-column flex-sm-row gap-2 align-items-sm-center ms-sm-auto py-2 py-sm-0">
                        <RouterLink :to="{ name: 'boards' }"
                            class="btn btn-sm btn-outline-secondary my-btn-outline-lift rounded-pill">
                            Boards</RouterLink>
                        <RouterLink :to="{ name: 'trash' }"
                            class="btn btn-sm btn-outline-danger my-btn-danger-lift rounded-pill">Trash</RouterLink>
                        <RouterLink :to="{ name: 'profile' }"
                            class="btn btn-sm btn-outline-secondary my-btn-outline-lift rounded-pill">
                            Profile</RouterLink>
                        <button class="btn btn-sm btn-primary my-btn-lift rounded-pill"
                            @click="authStore.logout()">Logout</button>
                    </div>
                </div>
            </div>
        </nav>
    </header>
</template>