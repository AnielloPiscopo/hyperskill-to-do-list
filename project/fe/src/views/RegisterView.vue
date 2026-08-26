<script setup lang="ts">
import { useRouter } from 'vue-router'
import RegisterForm from '@/components/domain/auth/RegisterForm.vue'

const router = useRouter()
function handleSuccess() {
    router.push({ name: 'login' })
}
</script>

<template>
    <div class="row justify-content-center">
        <div class="col-12 col-sm-8 col-md-5 col-lg-4">
            <div class="card shadow-sm p-4">
                <h1 class="h3 mb-4 text-center">Create your account</h1>
                <RegisterForm @success="handleSuccess" />
                <p class="text-center mt-3 mb-0">
                    <RouterLink :to="{ name: 'login' }">Already have an account? Sign in</RouterLink>
                </p>
            </div>
        </div>
    </div>
</template>