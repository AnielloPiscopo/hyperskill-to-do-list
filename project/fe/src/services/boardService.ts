import api from '@/services/api'
import { BOARD_ENDPOINTS } from '@/constants/endpoints'
import type { Board, BoardDetail, PatchedBoard, BoardPayload, PaginatedBoardList, SimpleMessageResponse, BulkIds } from '@/types'

export const boardService = {
    async getAll(params?: Record<string, string | number | boolean>): Promise<PaginatedBoardList> {
        const response = await api.get<PaginatedBoardList>(BOARD_ENDPOINTS.list, { params })
        return response.data
    },
    async getOne(id: number): Promise<BoardDetail> {
        const response = await api.get<BoardDetail>(BOARD_ENDPOINTS.detail(id))
        return response.data
    },
    async create(payload: BoardPayload): Promise<Board> {
        const response = await api.post<Board>(BOARD_ENDPOINTS.list, payload)
        return response.data
    },
    async update(id: number, payload: BoardPayload): Promise<Board> {
        const response = await api.put<Board>(BOARD_ENDPOINTS.detail(id), payload)
        return response.data
    },
    async partialUpdate(id: number, payload: PatchedBoard): Promise<Board> {
        const response = await api.patch<Board>(BOARD_ENDPOINTS.detail(id), payload)
        return response.data
    },
    async remove(id: number): Promise<void> {
        await api.delete(BOARD_ENDPOINTS.detail(id))
    },
    async archive(id: number): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(BOARD_ENDPOINTS.archive(id))
        return response.data
    },
    async restore(id: number, restoreTasks = false): Promise<SimpleMessageResponse> {
        const response = await api.post<SimpleMessageResponse>(BOARD_ENDPOINTS.restore(id), null, {
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