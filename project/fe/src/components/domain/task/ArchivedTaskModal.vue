<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import { useTaskStore } from '@/stores/taskStore'
import { boardService } from '@/services/boardService'
import type { Task } from '@/types'
import type { BoardDetail } from '@/types'

const props = defineProps<{ task: Task | null }>()
const emit = defineEmits<{ close: []; restored: []; requestDelete: [task: Task] }>()

const taskStore = useTaskStore()
const board = ref<BoardDetail | null>(null)
const modalRef = ref<HTMLElement | null>(null)
let modalInstance: Modal | null = null

onMounted(() => {
    if (modalRef.value) {
        modalInstance = new Modal(modalRef.value)
        modalRef.value.addEventListener('hidden.bs.modal', () => emit('close'))
    }
})

watch(
    () => props.task,
    async (task) => {
        board.value = null
        if (task) {
            if (task.board_slug) board.value = await boardService.getOne(task.board_slug)
            modalInstance?.show()
        } else {
            modalInstance?.hide()
        }
    }
)

async function handleRestore() {
    if (!props.task) return
    await taskStore.restoreTask(props.task.id)
    emit('restored')
    modalInstance?.hide()
}

function handleDeleteClick() {
    if (!props.task) return
    emit('requestDelete', props.task)
    modalInstance?.hide()
}
</script>

<template>
    <div ref="modalRef" class="modal fade" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div v-if="task" class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ task.title }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p v-if="board" class="text-muted small mb-3">Board: {{ board.title }}</p>
                    <p>{{ task.description }}</p>
                    <p class="my-text-mono text-muted mb-2">Deadline: {{ task.set_to_complete }}</p>
                    <span class="badge rounded-pill text-bg-light border me-2">{{ task.status }}</span>
                    <span class="badge rounded-pill"
                        :class="`my-badge-priority-${(task.priority ?? 'zero').toLowerCase()}`">
                        {{ task.priority }}
                    </span>

                    <div v-if="board?.is_archived" class="alert alert-warning mt-3 mb-0">
                        This task's board is archived. Restore the board first to bring this task back.
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary my-btn-outline-lift rounded-pill"
                        data-bs-dismiss="modal">
                        Close
                    </button>
                    <button type="button" class="btn btn-outline-danger my-btn-danger-lift rounded-pill"
                        @click="handleDeleteClick">
                        Delete
                    </button>
                    <button type="button" class="btn btn-primary my-btn-lift rounded-pill"
                        :disabled="board?.is_archived" @click="handleRestore">
                        Restore
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.my-badge-priority-high {
    background-color: var(--coral);
    color: #fff;
}

.my-badge-priority-medium {
    background-color: var(--sun);
    color: var(--ink);
}

.my-badge-priority-low {
    background-color: var(--teal);
    color: #fff;
}

.my-badge-priority-zero {
    background-color: var(--paper-border);
    color: var(--ink);
}
</style>