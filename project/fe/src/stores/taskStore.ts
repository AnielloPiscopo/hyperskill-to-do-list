import { defineStore } from 'pinia'
import { ref } from 'vue'
import { taskService } from '@/services/taskService'
import type { Task, TaskPayload, PatchedTask } from '@/types'

export const useTaskStore = defineStore('tasks', () => {
    const tasks = ref<Task[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function fetchTasks(params?: Record<string, string | number>) {
        loading.value = true
        error.value = null
        try {
            const data = await taskService.getAll(params)
            tasks.value = data.results
        } catch (e) {
            error.value = 'Errore nel caricamento dei task.'
        } finally {
            loading.value = false
        }
    }

    async function addTask(payload: TaskPayload) {
        const newTask = await taskService.create(payload)
        tasks.value.push(newTask)
    }

    async function updateTask(id: number, payload: PatchedTask) {
        const updated = await taskService.partialUpdate(id, payload)
        const index = tasks.value.findIndex((t) => t.id === id)
        if (index !== -1) tasks.value[index] = updated
    }

    async function removeTask(id: number) {
        await taskService.remove(id)
        tasks.value = tasks.value.filter((t) => t.id !== id)
    }

    async function archiveTask(id: number) {
        await taskService.archive(id)
        tasks.value = tasks.value.filter((t) => t.id !== id)
    }

    return { tasks, loading, error, fetchTasks, addTask, updateTask, removeTask, archiveTask }
})