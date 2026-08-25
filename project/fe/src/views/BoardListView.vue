<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useBoardStore } from '@/stores/boardStore'
import type { BoardPayload } from '@/types'

const boardStore = useBoardStore()
const newTitle = ref('')

onMounted(() => {
    boardStore.fetchBoards()
})

async function handleCreate() {
    if (!newTitle.value.trim()) return
    const payload: BoardPayload = { title: newTitle.value, description: '', color: '#1FA6A0' }
    await boardStore.addBoard(payload)
    newTitle.value = ''
}
</script>

<template>
    <div>
        <h1 class="h2 mb-4">My boards</h1>

        <form @submit.prevent="handleCreate" class="d-flex gap-2 mb-4">
            <input v-model="newTitle" type="text" class="form-control" placeholder="New board name" required />
            <button type="submit" class="btn btn-primary rounded-pill px-4">+ Create</button>
        </form>

        <p v-if="boardStore.loading" class="text-muted">Loading…</p>
        <p v-else-if="boardStore.error" class="alert alert-danger">{{ boardStore.error }}</p>

        <div v-else-if="boardStore.boards.length === 0" class="empty-state p-5 text-center">
            <p class="mb-0">You don't have any boards yet. Create one above to get started!</p>
        </div>

        <div v-else class="row g-3">
            <div v-for="board in boardStore.boards" :key="board.id" class="col-12 col-sm-6 col-lg-4">
                <div class="card board-card h-100 p-3" :style="{ '--board-color': board.color || '#1FA6A0' }">
                    <RouterLink :to="{ name: 'board-detail', params: { id: board.id } }"
                        class="text-decoration-none text-reset">
                        <h2 class="h5 mb-2">{{ board.title }}</h2>
                        <p class="text-muted small mb-0">{{ board.description || 'No description' }}</p>
                    </RouterLink>
                    <button class="btn btn-sm btn-outline-secondary rounded-pill mt-3 align-self-start"
                        @click="boardStore.archiveBoard(board.id)">
                        Archive
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>