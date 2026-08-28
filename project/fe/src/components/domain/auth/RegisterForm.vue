<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const emit = defineEmits<{ success: [] }>()
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
        emit('success')
    } catch (e) {
        error.value = 'Registration failed. Please check your details.'
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
            <label class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control" required />
        </div>
        <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" required />
        </div>
        <div class="mb-3">
            <label class="form-label">Confirm password</label>
            <input v-model="confirmPassword" type="password" class="form-control" required />
        </div>
        <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
        <button type="submit" class="btn btn-primary my-btn-lift w-100 rounded-pill" :disabled="loading">
            {{ loading ? 'Creating account…' : 'Create account' }}
        </button>
    </form>
</template>