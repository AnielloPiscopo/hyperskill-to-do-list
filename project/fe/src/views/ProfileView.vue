<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'
import type { Info } from '@/types'

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
        message.value = 'Password cambiata con successo.'
        oldPassword.value = ''
        newPassword.value = ''
        confirmNewPassword.value = ''
    } catch (e) {
        message.value = 'Errore nel cambio password.'
    }
}
</script>

<template>
    <main>
        <h1>Profile</h1>
        <p v-if="info">{{ info.username }} — {{ info.email }}</p>

        <form @submit.prevent="handleChangePassword">
            <input v-model="oldPassword" type="password" placeholder="Current password" required />
            <input v-model="newPassword" type="password" placeholder="New password" required />
            <input v-model="confirmNewPassword" type="password" placeholder="Confirm new password" required />
            <button type="submit">Change password</button>
        </form>
        <p v-if="message">{{ message }}</p>

        <button @click="authStore.logout()">Logout</button>
    </main>
</template>