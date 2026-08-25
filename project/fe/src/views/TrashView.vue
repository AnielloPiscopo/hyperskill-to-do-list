<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useTaskStore } from '@/stores/taskStore'
import { useBoardStore } from '@/stores/boardStore'
import ArchivedTaskModal from '@/components/domain/task/ArchivedTaskModal.vue'
import type { Task } from '@/types'

const taskStore = useTaskStore()
const boardStore = useBoardStore()
const selectedTask = ref<Task | null>(null)

onMounted(() => {
    taskStore.fetchTasks({ is_archived: true })
    boardStore.fetchBoards({ is_archived: true })
})

function openTask(task: Task) {
    selectedTask.value = task
}

async function handleRestored() {
    await taskStore.fetchTasks({ is_archived: true })
}
</script>

<template>
    <div>
        <h1 class="h2 mb-4">Trash</h1>

        <h2 class="h5 text-muted mb-2">Archived boards</h2>
        <div v-if="boardStore.boards.length === 0" class="empty-state p-4 text-center mb-4">
            <p class="mb-0 small">No archived boards.</p>
        </div>
        <ul v-else class="list-unstyled d-flex flex-column gap-2 mb-4">
            <li v-for="board in boardStore.boards" :key="board.id"
                class="card p-3 d-flex flex-row justify-content-between align-items-center">
                <span>{{ board.title }}</span>
                <button class="btn btn-sm btn-outline-secondary rounded-pill"
                    @click="boardStore.restoreBoard(board.id)">
                    Restore
                </button>
            </li>
        </ul>

        <h2 class="h5 text-muted mb-2">Archived tasks</h2>
        <div v-if="taskStore.tasks.length === 0" class="empty-state p-4 text-center">
            <p class="mb-0 small">No archived tasks.</p>
        </div>
        <ul v-else class="list-unstyled d-flex flex-column gap-2">
            <li v-for="task in taskStore.tasks" :key="task.id" class="task-row card p-3" role="button"
                @click="openTask(task)">
                {{ task.title }}
            </li>
        </ul>

        <ArchivedTaskModal :task="selectedTask" @close="selectedTask = null" @restored="handleRestored" />
    </div>
</template>