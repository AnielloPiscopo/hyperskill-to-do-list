import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services/authService'
import type { LoginRequest, Register } from '@/types'

export const useAuthStore = defineStore('auth', () => {
    const token = ref<string | null>(localStorage.getItem('token'))
    const isAuthenticated = computed(() => !!token.value)

    function setToken(newToken: string) {
        token.value = newToken
        localStorage.setItem('token', newToken)
    }

    function clearToken() {
        token.value = null
        localStorage.removeItem('token')
    }

    async function login(credentials: LoginRequest) {
        const { token: newToken } = await authService.login(credentials)
        setToken(newToken)
    }

    async function register(payload: Register) {
        await authService.register(payload)
    }

    async function logout() {
        try {
            await authService.logout()
        } finally {
            clearToken()
        }
    }

    window.addEventListener('auth:unauthorized', clearToken)

    return { token, isAuthenticated, login, register, logout, clearToken }
})