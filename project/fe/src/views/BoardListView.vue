<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useBoardStore } from '@/stores/boardStore'
import BoardFormModal from '@/components/domain/board/BoardFormModal.vue'
import BoardCard from '@/components/domain/board/BoardCard.vue'
import ConfirmModal from '@/components/base/ConfirmModal.vue'
import type { Board } from '@/types'

const boardStore = useBoardStore()
const formOpen = ref(false)
const editingBoard = ref<Board | null>(null)

const selectedBoardIds = ref<Set<number>>(new Set())
const hasSelectedBoards = computed(() => selectedBoardIds.value.size > 0)
const allSelected = computed(
    () => boardStore.boards.length > 0 && selectedBoardIds.value.size === boardStore.boards.length
)

const archiveAllConfirmOpen = ref(false)

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

function toggleSelect(id: number) {
    if (selectedBoardIds.value.has(id)) {
        selectedBoardIds.value.delete(id)
    } else {
        selectedBoardIds.value.add(id)
    }
}

function toggleSelectAll() {
    if (allSelected.value) {
        selectedBoardIds.value.clear()
    } else {
        selectedBoardIds.value = new Set(boardStore.boards.map((b) => b.id))
    }
}

async function handleArchiveSelected() {
    const ids = Array.from(selectedBoardIds.value)
    await boardStore.archiveAllBoards(ids)
    selectedBoardIds.value.clear()
}

async function handleArchiveAllConfirmed() {
    await boardStore.archiveAllBoards()
    selectedBoardIds.value.clear()
    archiveAllConfirmOpen.value = false
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

    <template v-else>
        <div class="d-flex justify-content-between align-items-center mb-3">
            <label class="d-flex align-items-center gap-2 mb-0 small">
                <input class="form-check-input" type="checkbox" :checked="allSelected" @change="toggleSelectAll" />
                Select all
            </label>
            <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-secondary my-btn-outline-lift rounded-pill"
                    :disabled="!hasSelectedBoards" @click="handleArchiveSelected">
                    Archive selected
                </button>
                <button class="btn btn-sm btn-outline-secondary my-btn-outline-lift rounded-pill"
                    @click="archiveAllConfirmOpen = true">
                    Archive all
                </button>
            </div>
        </div>

        <div class="row g-3">
            <div v-for="board in boardStore.boards" :key="board.id" class="col-12 col-sm-6 col-lg-4">
                <BoardCard :board="board" selectable :selected="selectedBoardIds.has(board.id)" @edit="openEdit"
                    @archive="boardStore.archiveBoard" @toggle-select="toggleSelect" />
            </div>
        </div>
    </template>

    <BoardFormModal :open="formOpen" :board="editingBoard" @close="handleFormClosed" />

    <ConfirmModal :open="archiveAllConfirmOpen" title="Archive all boards"
        message="This will archive every board you own. You can restore them later from Trash."
        confirm-text="Archive all" @confirm="handleArchiveAllConfirmed" @cancel="archiveAllConfirmOpen = false" />
</template>