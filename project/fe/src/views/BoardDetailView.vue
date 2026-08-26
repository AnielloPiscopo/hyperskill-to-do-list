<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useBoardStore } from '@/stores/boardStore'
import { useTaskStore } from '@/stores/taskStore'
import TaskFormModal from '@/components/domain/task/TaskFormModal.vue'
import TaskItem from '@/components/domain/task/TaskItem.vue'
import type { Task } from '@/types'

const route = useRoute()
const boardId = Number(route.params.id)

const boardStore = useBoardStore()
const taskStore = useTaskStore()

const formOpen = ref(false)
const editingTask = ref<Task | null>(null)

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

        <div v-else class="d-flex flex-column gap-2">
            <TaskItem v-for="task in boardStore.currentBoard.tasks" :key="task.id" :task="task" @edit="openEdit"
                @archive="handleArchiveTask" />
        </div>

        <TaskFormModal :open="formOpen" :task="editingTask" :board-id="boardId" @close="handleFormClosed" />
    </div>
</template>