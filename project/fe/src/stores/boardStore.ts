import { defineStore } from 'pinia'
import { ref } from 'vue'
import { boardService } from '@/services/boardService'
import type { Board, BoardDetail, BoardPayload, PatchedBoard } from '@/types'
import { isAxiosError } from 'axios'

export const useBoardStore = defineStore('boards', () => {
    const boards = ref<Board[]>([])
    const currentBoard = ref<BoardDetail | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function fetchBoards(params?: Record<string, string | number | boolean>) {
        loading.value = true
        error.value = null
        try {
            const data = await boardService.getAll(params)
            boards.value = data.results
        } catch (e) {
            if (isAxiosError(e) && e.response?.status === 404) {
                boards.value = []
            } else {
                error.value = 'Failded to load boards.'
            }
        } finally {
            loading.value = false
        }
    }

    async function fetchBoard(id: number) {
        loading.value = true
        error.value = null
        try {
            currentBoard.value = await boardService.getOne(id)
        } catch (e) {
            error.value = 'Failded to load boards.'
        } finally {
            loading.value = false
        }
    }

    async function addBoard(payload: BoardPayload) {
        const newBoard = await boardService.create(payload)
        boards.value.push(newBoard)
    }

    async function updateBoard(id: number, payload: PatchedBoard) {
        const updated = await boardService.partialUpdate(id, payload)
        const index = boards.value.findIndex((b) => b.id === id)
        if (index !== -1) boards.value[index] = updated
    }

    async function removeBoard(id: number) {
        await boardService.remove(id)
        boards.value = boards.value.filter((b) => b.id !== id)
    }

    async function archiveBoard(id: number) {
        await boardService.archive(id)
        boards.value = boards.value.filter((b) => b.id !== id)
    }

    async function restoreBoard(id: number, restoreTasks = false) {
        await boardService.restore(id, restoreTasks)
        boards.value = boards.value.filter((b) => b.id !== id)
    }

    return {
        boards,
        currentBoard,
        loading,
        error,
        fetchBoards,
        fetchBoard,
        addBoard,
        updateBoard,
        removeBoard,
        archiveBoard,
        restoreBoard
    }
})