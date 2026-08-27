import api from '@/services/api'
import { BOARD_ENDPOINTS } from '@/constants/endpoints'
import type { Board, BoardDetail, PatchedBoard, BoardPayload, PaginatedBoardList, SimpleMessageResponse, BulkIds } from '@/types'

export const boardService = {
    async getAll(params?: Record<string, string | number | boolean>): Promise<PaginatedBoardList> {
        const response = await api.get<PaginatedBoardList>(BOARD_ENDPOINTS.list, { params })
        return response.data
    },
    async getOne(slug: string): Promise<BoardDetail> {
        const response = await api.get<BoardDetail>(BOARD_ENDPOINTS.detail(slug))
        return response.data
    },
    async create(payload: BoardPayload): Promise<Board> {
        const response = await api.post<Board>(BOARD_ENDPOINTS.list, payload)
        return response.data
    },
    async update(slug: string, payload: BoardPayload): Promise<Board> {
        const response = await api.put<Board>(BOARD_ENDPOINTS.detail(slug), payload)
        return response.data
    },
    async partialUpdate(slug: string, payload: PatchedBoard): Promise<Board> {
        const response = await api.patch<Board>(BOARD_ENDPOINTS.detail(slug), payload)
        return response.data
    },
    async remove(slug: string): Promise<void> {
        await api.delete(BOARD_ENDPOINTS.detail(slug))
    },
    async archive(slug: string): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(BOARD_ENDPOINTS.archive(slug))
        return response.data
    },
    async restore(slug: string, restoreTasks = false): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(BOARD_ENDPOINTS.restore(slug), null, {
            params: { restore_tasks: restoreTasks }
        })
        return response.data
    },
    async archiveAll(payload: BulkIds = {}): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(BOARD_ENDPOINTS.archiveAll, payload)
        return response.data
    },
    async restoreAll(payload: BulkIds = {}, restoreTasks = false): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(BOARD_ENDPOINTS.restoreAll, payload, {
            params: { restore_tasks: restoreTasks }
        })
        return response.data
    }
}