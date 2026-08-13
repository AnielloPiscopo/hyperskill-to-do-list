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
    const payload: BoardPayload = { title: newTitle.value, description: '', color: '#FFFFFF' }
    await boardStore.addBoard(payload)
    newTitle.value = ''
}
</script>

<template>
    <main>
        <h1>My boards</h1>

        <form @submit.prevent="handleCreate">
            <input v-model="newTitle" type="text" placeholder="New board name" required />
            <button type="submit">Create</button>
        </form>

        <p v-if="boardStore.loading">Loading...</p>
        <p v-else-if="boardStore.error">{{ boardStore.error }}</p>

        <ul v-else>
            <li v-for="board in boardStore.boards" :key="board.id">
                <RouterLink :to="{ name: 'board-detail', params: { id: board.id } }">
                    {{ board.title }}
                </RouterLink>
                <button @click="boardStore.archiveBoard(board.id)">Archive</button>
            </li>
        </ul>
    </main>
</template>