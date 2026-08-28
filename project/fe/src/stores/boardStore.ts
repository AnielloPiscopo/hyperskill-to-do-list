import { defineStore } from 'pinia'
import { ref } from 'vue'
import { isAxiosError } from 'axios'
import { boardService } from '@/services/boardService'
import type { Board, BoardDetail, BoardPayload, PatchedBoard } from '@/types'

export const useBoardStore = defineStore('boards', () => {
    const boards = ref<Board[]>([])
    const currentBoard = ref<BoardDetail | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    const movedToSlug = ref<string | null>(null)

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
                error.value = 'Failed to load boards.'
            }
        } finally {
            loading.value = false
        }
    }

    async function fetchBoard(slug: string) {
        loading.value = true
        error.value = null
        movedToSlug.value = null
        try {
            currentBoard.value = await boardService.getOne(slug)
        } catch (e) {
            if (isAxiosError(e) && e.response?.status === 301 && e.response.data?.moved_to) {
                movedToSlug.value = e.response.data.moved_to
            } else {
                error.value = 'Failed to load board.'
            }
        } finally {
            loading.value = false
        }
    }

    async function addBoard(payload: BoardPayload) {
        const newBoard = await boardService.create(payload)
        boards.value.push(newBoard)
    }

    async function updateBoard(slug: string, payload: PatchedBoard) {
        const updated = await boardService.partialUpdate(slug, payload)
        const index = boards.value.findIndex((b) => b.slug === slug)
        if (index !== -1) boards.value[index] = updated
    }

    async function removeBoard(slug: string) {
        await boardService.remove(slug)
        boards.value = boards.value.filter((b) => b.slug !== slug)
    }

    async function archiveBoard(slug: string) {
        await boardService.archive(slug)
        boards.value = boards.value.filter((b) => b.slug !== slug)
    }

    async function restoreBoard(slug: string) {
        await boardService.restore(slug, true)
        boards.value = boards.value.filter((b) => b.slug !== slug)
    }

    async function deleteAllBoards(ids?: number[]) {
        await boardService.deleteAll(ids ? { ids } : {})
        if (ids) {
            boards.value = boards.value.filter((b) => !ids.includes(b.id))
        } else {
            boards.value = []
        }
    }

    async function archiveAllBoards(ids?: number[]) {
        await boardService.archiveAll(ids ? { ids } : {})
        if (ids) {
            boards.value = boards.value.filter((b) => !ids.includes(b.id))
        } else {
            boards.value = []
        }
    }

    async function restoreAllBoards(ids?: number[]) {
        await boardService.restoreAll(ids ? { ids } : {}, true)
        if (ids) {
            boards.value = boards.value.filter((b) => !ids.includes(b.id))
        } else {
            boards.value = []
        }
    }

    return {
        boards,
        currentBoard,
        loading,
        error,
        movedToSlug,
        fetchBoards,
        fetchBoard,
        addBoard,
        updateBoard,
        removeBoard,
        archiveBoard,
        restoreBoard,
        deleteAllBoards,
        archiveAllBoards,
        restoreAllBoards
    }
})