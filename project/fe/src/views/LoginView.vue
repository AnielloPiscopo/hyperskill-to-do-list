<script setup lang="ts">
import { useRouter } from 'vue-router'
import LoginForm from '@/components/domain/auth/LoginForm.vue'

const router = useRouter()

function handleSuccess() {
    router.push({ name: 'boards' })
}
</script>

<template>
    <div class="row justify-content-center">
        <div class="col-12 col-sm-8 col-md-5 col-lg-4">
            <div class="card shadow-sm p-4">
                <h1 class="h3 mb-4 text-center">Welcome back</h1>
                <LoginForm @success="handleSuccess" />
                <p class="text-center mt-3 mb-0">
                    <RouterLink :to="{ name: 'register' }">Don't have an account? Register</RouterLink>
                </p>
            </div>
        </div>
    </div>
</template>