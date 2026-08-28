<script setup lang="ts">
import { ref } from 'vue'
import { authService } from '@/services/authService'

const emit = defineEmits<{ success: [] }>()

const oldPassword = ref('')
const newPassword = ref('')
const confirmNewPassword = ref('')
const message = ref<string | null>(null)

async function handleSubmit() {
    message.value = null
    try {
        await authService.changePassword({
            old_password: oldPassword.value,
            new_password: newPassword.value,
            confirm_new_password: confirmNewPassword.value
        })
        emit('success')
    } catch (e) {
        message.value = 'Failed to change password.'
    }
}
</script>

<template>
    <form @submit.prevent="handleSubmit">
        <div class="mb-3">
            <input v-model="oldPassword" type="password" class="form-control" placeholder="Current password" required />
        </div>
        <div class="mb-3">
            <input v-model="newPassword" type="password" class="form-control" placeholder="New password" required />
        </div>
        <div class="mb-3">
            <input v-model="confirmNewPassword" type="password" class="form-control" placeholder="Confirm new password"
                required />
        </div>
        <div v-if="message" class="alert alert-warning py-2">{{ message }}</div>
        <button type="submit" class="btn btn-primary my-btn-lift rounded-pill px-4">Change password</button>
    </form>
</template>