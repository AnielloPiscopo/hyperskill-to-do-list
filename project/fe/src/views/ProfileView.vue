<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'
import ChangePasswordForm from '@/components/domain/auth/ChangePasswordForm.vue'
import type { Info } from '@/types'

const router = useRouter()
const authStore = useAuthStore()
const info = ref<Info | null>(null)

onMounted(async () => {
    info.value = await authService.about()
})

function handlePasswordChanged() {
    authStore.clearToken()
    router.push({ name: 'login' })
}
</script>

<template>
    <div class="row justify-content-center">
        <div class="col-12 col-md-6">
            <h1 class="h2 mb-4">Profile</h1>

            <div v-if="info" class="card p-4 mb-4">
                <p class="mb-1 text-muted small">Signed in as</p>
                <p class="h5 mb-0">{{ info.username }}</p>
                <p class="text-muted mb-0">{{ info.email }}</p>
            </div>

            <section class="card p-4">
                <h2 class="h5 mb-3">Change password</h2>
                <ChangePasswordForm @success="handlePasswordChanged" />
            </section>

            <button class="btn btn-outline-secondary rounded-pill mt-4" @click="authStore.logout()">Logout</button>
        </div>
    </div>
</template>