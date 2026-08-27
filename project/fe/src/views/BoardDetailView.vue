<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBoardStore } from '@/stores/boardStore'
import { useTaskStore } from '@/stores/taskStore'
import TaskFormModal from '@/components/domain/task/TaskFormModal.vue'
import TaskItem from '@/components/domain/task/TaskItem.vue'
import type { Task } from '@/types'

const route = useRoute()
const router = useRouter()

const boardStore = useBoardStore()
const taskStore = useTaskStore()

const formOpen = ref(false)
const editingTask = ref<Task | null>(null)

async function loadBoard() {
    const slug = route.params.slug as string
    await boardStore.fetchBoard(slug)

    if (boardStore.movedToSlug) {
        router.replace({ name: 'board-detail', params: { slug: boardStore.movedToSlug } })
    }
}

onMounted(loadBoard)

watch(() => route.params.slug, loadBoard)

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
    if (boardStore.currentBoard) await boardStore.fetchBoard(boardStore.currentBoard.slug)
}

async function handleArchiveTask(taskId: number) {
    await taskStore.archiveTask(taskId)
    if (boardStore.currentBoard) await boardStore.fetchBoard(boardStore.currentBoard.slug)
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
            <TaskItem v-for="task in boardStore.currentBoard.tasks" :key="task.id" :task="task" @select="openEdit"
                @archive="handleArchiveTask" />
        </div>

        <TaskFormModal :open="formOpen" :task="editingTask" :board-id="boardStore.currentBoard.id"
            @close="handleFormClosed" />
    </div>
</template>