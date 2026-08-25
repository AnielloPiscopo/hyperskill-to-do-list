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

const priorityColor: Record<string, string> = {
    HIGH: 'var(--coral)',
    MEDIUM: 'var(--sun)',
    LOW: 'var(--teal)',
    ZERO: 'var(--paper-border)'
}

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
    <div>
        <p v-if="boardStore.loading" class="text-muted">Loading…</p>
        <p v-else-if="boardStore.error" class="alert alert-danger">{{ boardStore.error }}</p>

        <div v-else-if="boardStore.currentBoard">
            <h1 class="h2 mb-1">{{ boardStore.currentBoard.title }}</h1>
            <p class="text-muted mb-4">{{ boardStore.currentBoard.description }}</p>

            <form @submit.prevent="handleAddTask" class="d-flex gap-2 mb-4">
                <input v-model="newTaskTitle" type="text" class="form-control" placeholder="New task" required />
                <button type="submit" class="btn btn-primary rounded-pill px-4">+ Add</button>
            </form>

            <div v-if="boardStore.currentBoard.tasks.length === 0" class="empty-state p-5 text-center">
                <p class="mb-0">No tasks yet — add your first one above.</p>
            </div>

            <ul v-else class="list-unstyled d-flex flex-column gap-2">
                <li v-for="task in boardStore.currentBoard.tasks" :key="task.id"
                    class="task-row card p-3 d-flex flex-row justify-content-between align-items-center"
                    :style="{ '--priority-color': priorityColor[task.priority ?? 'ZERO'] }">
                    <div>
                        <span class="fw-medium">{{ task.title }}</span>
                        <span class="badge rounded-pill ms-2 text-mono"
                            :class="task.status === 'DONE' ? 'text-bg-success' : 'text-bg-light border'">
                            {{ task.status }}
                        </span>
                    </div>
                    <button class="btn btn-sm btn-outline-secondary rounded-pill" @click="handleArchiveTask(task.id)">
                        Archive
                    </button>
                </li>
            </ul>
        </div>
    </div>
</template>