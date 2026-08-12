import api from '@/services/api'
import { AUTH_ENDPOINTS } from '@/constants/endpoints'
import type { LoginRequest, TokenResponse, Register, Info, ChangePassword, SimpleMessageResponse } from '@/types'

export const authService = {
    async login(payload: LoginRequest): Promise<TokenResponse> {
        const response = await api.post<TokenResponse>(AUTH_ENDPOINTS.login, payload)
        return response.data
    },
    async register(payload: Register): Promise<Info> {
        const response = await api.post<Info>(AUTH_ENDPOINTS.register, payload)
        return response.data
    },
    async logout(): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(AUTH_ENDPOINTS.logout)
        return response.data
    },
    async about(): Promise<Info> {
        const response = await api.get<Info>(AUTH_ENDPOINTS.about)
        return response.data
    },
    async changePassword(payload: ChangePassword): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(AUTH_ENDPOINTS.changePassword, payload)
        return response.data
    }
}