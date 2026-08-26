<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useBoardStore } from '@/stores/boardStore'
import { useTaskStore } from '@/stores/taskStore'
import TaskFormModal from '@/components/domain/task/TaskFormModal.vue'
import type { Task } from '@/types'

const route = useRoute()
const boardId = Number(route.params.id)

const boardStore = useBoardStore()
const taskStore = useTaskStore()

const formOpen = ref(false)
const editingTask = ref<Task | null>(null)

const priorityColor: Record<string, string> = {
    HIGH: 'var(--coral)',
    MEDIUM: 'var(--sun)',
    LOW: 'var(--teal)',
    ZERO: 'var(--paper-border)'
}

onMounted(() => {
    boardStore.fetchBoard(boardId)
})

function openCreate() {
    editingTask.value = null
    formOpen.value = true
}

function openEdit(task: Task) {
    editingTask.value = task
    formOpen.value = true
}

async function handleFormClosed() {
    formOpen.value = false
    await boardStore.fetchBoard(boardId)
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
            <div class="d-flex justify-content-between align-items-center mb-1">
                <h1 class="h2 mb-0">{{ boardStore.currentBoard.title }}</h1>
                <button class="btn btn-primary my-btn-lift rounded-pill px-4" @click="openCreate">+ New task</button>
            </div>
            <p class="text-muted mb-4">{{ boardStore.currentBoard.description }}</p>

            <div v-if="boardStore.currentBoard.tasks.length === 0" class="my-empty-state p-5 text-center">
                <p class="mb-0">No tasks yet — create your first one above.</p>
            </div>

            <ul v-else class="list-unstyled d-flex flex-column gap-2">
                <li v-for="task in boardStore.currentBoard.tasks" :key="task.id"
                    class="my-task-row card p-3 d-flex flex-column flex-sm-row justify-content-between align-items-start align-items-sm-center gap-2"
                    :style="{ '--priority-color': priorityColor[task.priority ?? 'ZERO'] }" role="button"
                    @click="openEdit(task)">
                    <div>
                        <span class="fw-medium">{{ task.title }}</span>
                        <span class="badge rounded-pill ms-2 my-text-mono" :class="{
                            'text-bg-light border': task.status === 'TODO',
                            'text-bg-info': task.status === 'IN_PROGRESS',
                            'text-bg-success': task.status === 'DONE'
                        }">
                            {{ task.status }}
                        </span>
                    </div>
                    <button class="btn btn-sm btn-outline-secondary rounded-pill"
                        @click.stop="handleArchiveTask(task.id)">
                        Archive
                    </button>
                </li>
            </ul>

            <TaskFormModal :open="formOpen" :task="editingTask" :board-id="boardId" @close="handleFormClosed" />
        </div>
    </div>
</template>