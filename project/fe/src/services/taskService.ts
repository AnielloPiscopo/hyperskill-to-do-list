import api from '@/services/api'
import { TASK_ENDPOINTS } from '@/constants/endpoints'
import type { Task, PatchedTask, TaskPayload, TaskMove, PaginatedTaskList, SimpleMessageResponse, BulkIds } from '@/types'

export const taskService = {
    async getAll(params?: Record<string, string | number | boolean>): Promise<PaginatedTaskList> {
        const response = await api.get<PaginatedTaskList>(TASK_ENDPOINTS.list, { params })
        return response.data
    },
    async getOne(id: number): Promise<Task> {
        const response = await api.get<Task>(TASK_ENDPOINTS.detail(id))
        return response.data
    },
    async create(payload: TaskPayload): Promise<Task> {
        const response = await api.post<Task>(TASK_ENDPOINTS.list, payload)
        return response.data
    },
    async update(id: number, payload: TaskPayload): Promise<Task> {
        const response = await api.put<Task>(TASK_ENDPOINTS.detail(id), payload)
        return response.data
    },
    async partialUpdate(id: number, payload: PatchedTask): Promise<Task> {
        const response = await api.patch<Task>(TASK_ENDPOINTS.detail(id), payload)
        return response.data
    },
    async remove(id: number): Promise<void> {
        await api.delete(TASK_ENDPOINTS.detail(id))
    },
    async archive(id: number): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(TASK_ENDPOINTS.archive(id))
        return response.data
    },
    async restore(id: number): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(TASK_ENDPOINTS.restore(id))
        return response.data
    },
    async archiveAll(payload: BulkIds = {}): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(TASK_ENDPOINTS.archiveAll, payload)
        return response.data
    },
    async restoreAll(payload: BulkIds = {}): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(TASK_ENDPOINTS.restoreAll, payload)
        return response.data
    },
    async move(payload: TaskMove): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(TASK_ENDPOINTS.move, payload)
        return response.data
    }
}