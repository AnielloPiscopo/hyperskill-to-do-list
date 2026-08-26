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
        error.value = 'Registration failed. Please check your details.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="row justify-content-center">
        <div class="col-12 col-sm-8 col-md-5 col-lg-4">
            <div class="card shadow-sm p-4">
                <h1 class="h3 mb-4 text-center">Create your account</h1>
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
                <p class="text-center mt-3 mb-0">
                    <RouterLink :to="{ name: 'login' }">Already have an account? Sign in</RouterLink>
                </p>
            </div>
        </div>
    </div>
</template>