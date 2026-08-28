<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import { useTaskStore } from '@/stores/taskStore'
import type { Task, TaskPayload, PatchedTask, TaskStatus, TaskPriority } from '@/types'

const props = defineProps<{ open: boolean; task: Task | null; boardId: number }>()
const emit = defineEmits<{ close: [] }>()

const taskStore = useTaskStore()
const modalRef = ref<HTMLElement | null>(null)
let modalInstance: Modal | null = null

const title = ref('')
const description = ref('')
const goalSetDate = ref('')
const setToComplete = ref('')
const status = ref<TaskStatus>('TODO')
const priority = ref<TaskPriority>('ZERO')
const error = ref<string | null>(null)
const saving = ref(false)

const isEditMode = computed(() => props.task !== null)

function resetForm() {
    error.value = null
    if (props.task) {
        title.value = props.task.title
        description.value = props.task.description ?? ''
        goalSetDate.value = props.task.goal_set_date
        setToComplete.value = props.task.set_to_complete
        status.value = props.task.status ?? 'TODO'
        priority.value = props.task.priority ?? 'ZERO'
    } else {
        const today = new Date().toISOString().slice(0, 10)
        title.value = ''
        description.value = ''
        goalSetDate.value = today
        setToComplete.value = today
        status.value = 'TODO'
        priority.value = 'ZERO'
    }
}

onMounted(() => {
    if (modalRef.value) {
        modalInstance = new Modal(modalRef.value)
        modalRef.value.addEventListener('hidden.bs.modal', () => emit('close'))
    }
})

watch(
    () => props.open,
    (open) => {
        if (open) {
            resetForm()
            modalInstance?.show()
        } else {
            modalInstance?.hide()
        }
    }
)

async function handleSubmit() {
    if (!title.value.trim()) {
        error.value = 'Title is required.'
        return
    }
    error.value = null
    saving.value = true
    try {
        if (isEditMode.value && props.task) {
            const payload: PatchedTask = {
                title: title.value,
                description: description.value,
                goal_set_date: goalSetDate.value,
                set_to_complete: setToComplete.value,
                status: status.value,
                priority: priority.value
            }
            await taskStore.updateTask(props.task.id, payload)
        } else {
            const payload: TaskPayload = {
                title: title.value,
                description: description.value,
                goal_set_date: goalSetDate.value,
                set_to_complete: setToComplete.value,
                status: status.value,
                priority: priority.value,
                board: props.boardId
            }
            await taskStore.addTask(payload)
        }
        modalInstance?.hide()
    } catch (e) {
        error.value = 'Failed to save task. Check the dates and try again.'
    } finally {
        saving.value = false
    }
}
</script>

<template>
    <div ref="modalRef" class="modal fade" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ isEditMode ? 'Edit task' : 'New task' }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <form @submit.prevent="handleSubmit">
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Title</label>
                            <input v-model="title" type="text" class="form-control" required />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            <textarea v-model="description" class="form-control" rows="3"></textarea>
                        </div>
                        <div class="row g-2 mb-3">
                            <div class="col-6">
                                <label class="form-label">Start date</label>
                                <input v-model="goalSetDate" type="date" class="form-control" required />
                            </div>
                            <div class="col-6">
                                <label class="form-label">Deadline</label>
                                <input v-model="setToComplete" type="date" class="form-control" required />
                            </div>
                        </div>
                        <div class="row g-2 mb-3">
                            <div class="col-6">
                                <label class="form-label">Status</label>
                                <select v-model="status" class="form-select">
                                    <option value="TODO">To do</option>
                                    <option value="IN_PROGRESS">In progress</option>
                                    <option v-if="isEditMode" value="DONE">Done</option>
                                </select>
                            </div>
                            <div class="col-6">
                                <label class="form-label">Priority</label>
                                <select v-model="priority" class="form-select">
                                    <option value="ZERO">None</option>
                                    <option value="LOW">Low</option>
                                    <option value="MEDIUM">Medium</option>
                                    <option value="HIGH">High</option>
                                </select>
                            </div>
                        </div>
                        <div v-if="error" class="alert alert-danger py-2 mb-0">{{ error }}</div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary rounded-pill" data-bs-dismiss="modal">
                            Cancel
                        </button>
                        <button type="submit" class="btn btn-primary my-btn-lift rounded-pill" :disabled="saving">
                            {{ isEditMode ? 'Save changes' : 'Create task' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>