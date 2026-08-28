<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const emit = defineEmits<{ success: [] }>()
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
        emit('success')
    } catch (e) {
        error.value = 'Invalid credentials.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <form @submit.prevent="handleSubmit">
        <div class="mb-3">
            <label class="form-label">Username</label>
            <input v-model="username" type="text" class="form-control" required />
        </div>
        <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" required />
        </div>
        <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
        <button type="submit" class="btn btn-primary my-btn-lift w-100 rounded-pill" :disabled="loading">
            {{ loading ? 'Signing in…' : 'Sign in' }}
        </button>
    </form>
</template>