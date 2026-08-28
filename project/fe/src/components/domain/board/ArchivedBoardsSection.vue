<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useBoardStore } from '@/stores/boardStore'
import { useTaskStore } from '@/stores/taskStore'
import BoardCard from '@/components/domain/board/BoardCard.vue'
import ConfirmModal from '@/components/base/ConfirmModal.vue'
import type { Board } from '@/types'

const boardStore = useBoardStore()
const taskStore = useTaskStore()

const selectedIds = ref<Set<number>>(new Set())
const hasSelected = computed(() => selectedIds.value.size > 0)
const allSelected = computed(
    () => boardStore.boards.length > 0 && selectedIds.value.size === boardStore.boards.length
)

const pendingDeleteBoard = ref<Board | null>(null)
const emptyConfirmOpen = ref(false)

onMounted(() => {
    boardStore.fetchBoards({ is_archived: true })
})

function toggleSelect(id: number) {
    if (selectedIds.value.has(id)) selectedIds.value.delete(id)
    else selectedIds.value.add(id)
}

function toggleSelectAll() {
    selectedIds.value = allSelected.value ? new Set() : new Set(boardStore.boards.map((b) => b.id))
}

async function refreshTasks() {
    await taskStore.fetchTasks({ is_archived: true })
}

async function handleRestore(slug: string) {
    await boardStore.restoreBoard(slug)
    await refreshTasks()
}

async function handleRestoreSelected() {
    const ids = Array.from(selectedIds.value)
    await boardStore.restoreAllBoards(ids)
    selectedIds.value.clear()
    await refreshTasks()
}

async function handleRestoreAll() {
    await boardStore.restoreAllBoards()
    selectedIds.value.clear()
    await refreshTasks()
}

async function handleDeleteConfirmed() {
    if (!pendingDeleteBoard.value) return
    await boardStore.removeBoard(pendingDeleteBoard.value.slug)
    pendingDeleteBoard.value = null
    await refreshTasks()
}

async function handleDeleteSelected() {
    const ids = Array.from(selectedIds.value)
    if (!confirm(`Permanently delete ${ids.length} selected board(s)? This cannot be undone.`)) return
    await boardStore.deleteAllBoards(ids)
    selectedIds.value.clear()
    await refreshTasks()
}

async function handleEmptyConfirmed() {
    await boardStore.deleteAllBoards()
    selectedIds.value.clear()
    emptyConfirmOpen.value = false
    await refreshTasks()
}
</script>

<template>
    <div>
        <h2 class="h5 text-muted mb-2">Archived boards</h2>

        <div v-if="boardStore.boards.length === 0" class="my-empty-state p-4 text-center">
            <p class="mb-0 small">No archived boards.</p>
        </div>

        <template v-else>
            <div class="d-flex justify-content-between align-items-center mb-2">
                <label class="d-flex align-items-center gap-2 mb-0 small">
                    <input class="form-check-input" type="checkbox" :checked="allSelected" @change="toggleSelectAll" />
                    Select all
                </label>
                <div class="d-flex gap-2 flex-wrap">
                    <button class="btn btn-sm btn-outline-secondary my-btn-outline-lift rounded-pill"
                        :disabled="!hasSelected" @click="handleRestoreSelected">
                        Restore selected
                    </button>
                    <button class="btn btn-sm btn-outline-secondary my-btn-outline-lift rounded-pill"
                        @click="handleRestoreAll">
                        Restore all
                    </button>
                    <button class="btn btn-sm btn-outline-danger my-btn-danger-lift rounded-pill"
                        :disabled="!hasSelected" @click="handleDeleteSelected">
                        Delete selected
                    </button>
                    <button class="btn btn-sm btn-outline-danger my-btn-danger-lift rounded-pill"
                        @click="emptyConfirmOpen = true">
                        Empty
                    </button>
                </div>
            </div>

            <div class="row g-3">
                <div v-for="board in boardStore.boards" :key="board.id" class="col-12 col-sm-6 col-lg-4">
                    <BoardCard :board="board" archived selectable :selected="selectedIds.has(board.id)"
                        @restore="handleRestore" @delete="pendingDeleteBoard = $event" @toggle-select="toggleSelect" />
                </div>
            </div>
        </template>

        <ConfirmModal :open="pendingDeleteBoard !== null" title="Delete board"
            :message="`Permanently delete &quot;${pendingDeleteBoard?.title}&quot;? This cannot be undone.`"
            confirm-text="Delete" @confirm="handleDeleteConfirmed" @cancel="pendingDeleteBoard = null" />

        <ConfirmModal :open="emptyConfirmOpen" title="Empty archived boards"
            message="This will permanently delete ALL archived boards. This cannot be undone." confirm-text="Delete all"
            require-typed-confirmation="DELETE" @confirm="handleEmptyConfirmed" @cancel="emptyConfirmOpen = false" />
    </div>
</template>