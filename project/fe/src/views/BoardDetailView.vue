<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useBoardStore } from '@/stores/boardStore'
import { useTaskStore } from '@/stores/taskStore'
import type { TaskPayload } from '@/types'

const route = useRoute()
const boardId = Number(route.params.id)

const boardStore = useBoardStore()
const taskStore = useTaskStore()
const newTaskTitle = ref('')

onMounted(() => {
    boardStore.fetchBoard(boardId)
})

async function handleAddTask() {
    if (!newTaskTitle.value.trim()) return
    const payload: TaskPayload = {
        title: newTaskTitle.value,
        description: '',
        goal_set_date: new Date().toISOString().slice(0, 10),
        set_to_complete: new Date().toISOString().slice(0, 10),
        status: 'TODO',
        priority: 'ZERO',
        board: boardId
    }
    await taskStore.addTask(payload)
    await boardStore.fetchBoard(boardId)
    newTaskTitle.value = ''
}

async function handleArchiveTask(taskId: number) {
    await taskStore.archiveTask(taskId)
    await boardStore.fetchBoard(boardId)
}
</script>

<template>
    <main>
        <p v-if="boardStore.loading">Loading...</p>
        <p v-else-if="boardStore.error">{{ boardStore.error }}</p>

        <div v-else-if="boardStore.currentBoard">
            <h1>{{ boardStore.currentBoard.title }}</h1>
            <p>{{ boardStore.currentBoard.description }}</p>

            <form @submit.prevent="handleAddTask">
                <input v-model="newTaskTitle" type="text" placeholder="New task" required />
                <button type="submit">Add</button>
            </form>

            <ul>
                <li v-for="task in boardStore.currentBoard.tasks" :key="task.id">
                    {{ task.title }} — {{ task.status }}
                    <button @click="handleArchiveTask(task.id)">Archive</button>
                </li>
            </ul>
        </div>
    </main>
</template>