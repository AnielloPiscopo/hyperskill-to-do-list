<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref<string | null>(null)
const loading = ref(false)

async function handleSubmit() {
    error.value = null
    loading.value = true
    try {
        await authStore.login({ username: username.value, password: password.value })
        router.push({ name: 'boards' })
    } catch (e) {
        error.value = 'Credenziali non valide.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <main>
        <form @submit.prevent="handleSubmit">
            <h1>Login</h1>
            <input v-model="username" type="text" placeholder="Username" required />
            <input v-model="password" type="password" placeholder="Password" required />
            <p v-if="error">{{ error }}</p>
            <button type="submit" :disabled="loading">{{ loading ? 'Signing in...' : 'Sign in' }}</button>
            <RouterLink :to="{ name: 'register' }">Don't have an account? Register</RouterLink>
        </form>
    </main>
</template>