<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'
import type { Info } from '@/types'

const router = useRouter()
const authStore = useAuthStore()
const info = ref<Info | null>(null)

const oldPassword = ref('')
const newPassword = ref('')
const confirmNewPassword = ref('')
const message = ref<string | null>(null)

onMounted(async () => {
    info.value = await authService.about()
})

async function handleChangePassword() {
    message.value = null
    try {
        await authService.changePassword({
            old_password: oldPassword.value,
            new_password: newPassword.value,
            confirm_new_password: confirmNewPassword.value
        })
        // Backend invalidates the token on password change, so the user must log in again
        authStore.clearToken()
        router.push({ name: 'login' })
    } catch (e) {
        message.value = 'Failed to change password.'
    }
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

            <div class="card p-4">
                <h2 class="h5 mb-3">Change password</h2>
                <form @submit.prevent="handleChangePassword">
                    <div class="mb-3">
                        <input v-model="oldPassword" type="password" class="form-control" placeholder="Current password"
                            required />
                    </div>
                    <div class="mb-3">
                        <input v-model="newPassword" type="password" class="form-control" placeholder="New password"
                            required />
                    </div>
                    <div class="mb-3">
                        <input v-model="confirmNewPassword" type="password" class="form-control"
                            placeholder="Confirm new password" required />
                    </div>
                    <div v-if="message" class="alert alert-warning py-2">{{ message }}</div>
                    <button type="submit" class="btn btn-primary rounded-pill px-4">Change password</button>
                </form>
            </div>

            <button class="btn btn-outline-secondary rounded-pill mt-4" @click="authStore.logout()">Logout</button>
        </div>
    </div>
</template>