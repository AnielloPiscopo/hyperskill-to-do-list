<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useTaskStore } from '@/stores/taskStore'
import { useBoardStore } from '@/stores/boardStore'
import TaskItem from '@/components/domain/task/TaskItem.vue'
import ArchivedTaskModal from '@/components/domain/task/ArchivedTaskModal.vue'
import ConfirmModal from '@/components/base/ConfirmModal.vue'
import type { Task } from '@/types'

const taskStore = useTaskStore()
const boardStore = useBoardStore()

const selectedIds = ref<Set<number>>(new Set())
const hasSelected = computed(() => selectedIds.value.size > 0)
const allSelected = computed(
    () => taskStore.tasks.length > 0 && selectedIds.value.size === taskStore.tasks.length
)

const archivedBoardSlugs = computed(() => new Set(boardStore.boards.map((b) => b.slug)))

const selectedTask = ref<Task | null>(null)
const pendingDeleteTask = ref<Task | null>(null)
const emptyConfirmOpen = ref(false)

onMounted(() => {
    taskStore.fetchTasks({ is_archived: true })
})

function toggleSelect(id: number) {
    if (selectedIds.value.has(id)) selectedIds.value.delete(id)
    else selectedIds.value.add(id)
}

function toggleSelectAll() {
    selectedIds.value = allSelected.value ? new Set() : new Set(taskStore.tasks.map((t) => t.id))
}

function openTask(task: Task) {
    selectedTask.value = task
}

async function handleRestoredFromModal() {
    await taskStore.fetchTasks({ is_archived: true })
}

async function handleRestoreSelected() {
    const ids = Array.from(selectedIds.value)
    await taskStore.restoreAllTasks(ids)
    selectedIds.value.clear()
}

async function handleRestoreAll() {
    await taskStore.restoreAllTasks()
    selectedIds.value.clear()
}

async function handleDeleteConfirmed() {
    if (!pendingDeleteTask.value) return
    await taskStore.removeTask(pendingDeleteTask.value.id)
    pendingDeleteTask.value = null
}

async function handleDeleteSelected() {
    const ids = Array.from(selectedIds.value)
    if (!confirm(`Permanently delete ${ids.length} selected task(s)? This cannot be undone.`)) return
    await taskStore.deleteAllTasks(ids)
    selectedIds.value.clear()
}

async function handleEmptyConfirmed() {
    await taskStore.deleteAllTasks()
    selectedIds.value.clear()
    emptyConfirmOpen.value = false
}
</script>

<template>
    <div>
        <h2 class="h5 text-muted mb-2">Archived tasks</h2>

        <div v-if="taskStore.tasks.length === 0" class="my-empty-state p-4 text-center">
            <p class="mb-0 small">No archived tasks.</p>
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

            <div class="d-flex flex-column gap-2">
                <TaskItem v-for="task in taskStore.tasks" :key="task.id" :task="task" archived
                    :selected="selectedIds.has(task.id)"
                    :board-archived="!!task.board_slug && archivedBoardSlugs.has(task.board_slug)" @select="openTask"
                    @restore="taskStore.restoreTask" @delete="pendingDeleteTask = $event"
                    @toggle-select="toggleSelect" />
            </div>
        </template>

        <ArchivedTaskModal :task="selectedTask" @close="selectedTask = null" @restored="handleRestoredFromModal"
            @request-delete="pendingDeleteTask = $event" />

        <ConfirmModal :open="pendingDeleteTask !== null" title="Delete task"
            :message="`Permanently delete &quot;${pendingDeleteTask?.title}&quot;? This cannot be undone.`"
            confirm-text="Delete" @confirm="handleDeleteConfirmed" @cancel="pendingDeleteTask = null" />

        <ConfirmModal :open="emptyConfirmOpen" title="Empty archived tasks"
            message="This will permanently delete ALL archived tasks. This cannot be undone." confirm-text="Delete all"
            require-typed-confirmation="DELETE" @confirm="handleEmptyConfirmed" @cancel="emptyConfirmOpen = false" />
    </div>
</template>