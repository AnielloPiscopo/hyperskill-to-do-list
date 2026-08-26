<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useTaskStore } from '@/stores/taskStore'
import { useBoardStore } from '@/stores/boardStore'
import ArchivedTaskModal from '@/components/domain/task/ArchivedTaskModal.vue'
import TaskItem from '@/components/domain/task/TaskItem.vue'
import BoardCard from '@/components/domain/board/BoardCard.vue'
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
    <h1 class="h2 mb-4">Trash</h1>

    <section class="mb-4">
        <h2 class="h5 text-muted mb-2">Archived boards</h2>
        <div v-if="boardStore.boards.length === 0" class="my-empty-state p-4 text-center">
            <p class="mb-0 small">No archived boards.</p>
        </div>
        <div v-else class="row g-3">
            <div v-for="board in boardStore.boards" :key="board.id" class="col-12 col-sm-6 col-lg-4">
                <BoardCard :board="board" archived @restore="boardStore.restoreBoard" />
            </div>
        </div>
    </section>

    <section>
        <h2 class="h5 text-muted mb-2">Archived tasks</h2>
        <div v-if="taskStore.tasks.length === 0" class="my-empty-state p-4 text-center">
            <p class="mb-0 small">No archived tasks.</p>
        </div>
        <div v-else class="d-flex flex-column gap-2">
            <TaskItem v-for="task in taskStore.tasks" :key="task.id" :task="task" archived @select="openTask" />
        </div>
    </section>

    <ArchivedTaskModal :task="selectedTask" @close="selectedTask = null" @restored="handleRestored" />
</template>