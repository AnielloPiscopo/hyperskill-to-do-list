<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useBoardStore } from '@/stores/boardStore'
import BoardFormModal from '@/components/domain/board/BoardFormModal.vue'
import BoardCard from '@/components/domain/board/BoardCard.vue'
import type { Board } from '@/types'

const boardStore = useBoardStore()
const formOpen = ref(false)
const editingBoard = ref<Board | null>(null)

onMounted(() => {
    boardStore.fetchBoards()
})

function openCreate() {
    editingBoard.value = null
    formOpen.value = true
}

function openEdit(board: Board) {
    editingBoard.value = board
    formOpen.value = true
}

async function handleFormClosed() {
    formOpen.value = false
    await boardStore.fetchBoards()
}
</script>

<template>
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h2 mb-0">My boards</h1>
        <button class="btn btn-primary my-btn-lift rounded-pill px-4" @click="openCreate">+ New board</button>
    </div>

    <p v-if="boardStore.loading" class="text-muted">Loading…</p>
    <p v-else-if="boardStore.error" class="alert alert-danger">{{ boardStore.error }}</p>

    <div v-else-if="boardStore.boards.length === 0" class="my-empty-state p-5 text-center">
        <p class="mb-0">You don't have any boards yet. Create one above to get started!</p>
    </div>

    <div v-else class="row g-3">
        <div v-for="board in boardStore.boards" :key="board.id" class="col-12 col-sm-6 col-lg-4">
            <BoardCard :board="board" @edit="openEdit" @archive="boardStore.archiveBoard" />
        </div>
    </div>

    <BoardFormModal :open="formOpen" :board="editingBoard" @close="handleFormClosed" />
</template>