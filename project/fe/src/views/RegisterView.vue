<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref<string | null>(null)
const loading = ref(false)

async function handleSubmit() {
    error.value = null
    loading.value = true
    try {
        await authStore.register({
            username: username.value,
            email: email.value,
            password: password.value,
            confirm_password: confirmPassword.value
        })
        router.push({ name: 'login' })
    } catch (e) {
        error.value = 'Errore nella registrazione. Controlla i dati inseriti.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <main>
        <form @submit.prevent="handleSubmit">
            <h1>Register</h1>
            <input v-model="username" type="text" placeholder="Username" required />
            <input v-model="email" type="email" placeholder="Email" />
            <input v-model="password" type="password" placeholder="Password" required />
            <input v-model="confirmPassword" type="password" placeholder="Confirm password" required />
            <p v-if="error">{{ error }}</p>
            <button type="submit" :disabled="loading">{{ loading ? 'Creating account...' : 'Create account' }}</button>
            <RouterLink :to="{ name: 'login' }">Already have an account? Sign in</RouterLink>
        </form>
    </main>
</template>