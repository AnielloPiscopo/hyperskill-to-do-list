<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import { useBoardStore } from '@/stores/boardStore'
import type { Board, BoardPayload, PatchedBoard } from '@/types'

const props = defineProps<{ open: boolean; board: Board | null }>()
const emit = defineEmits<{ close: [] }>()

const boardStore = useBoardStore()
const modalRef = ref<HTMLElement | null>(null)
let modalInstance: Modal | null = null

const title = ref('')
const description = ref('')
const color = ref('#1FA6A0')
const error = ref<string | null>(null)
const saving = ref(false)

const isEditMode = computed(() => props.board !== null)

function resetForm() {
    error.value = null
    if (props.board) {
        title.value = props.board.title
        description.value = props.board.description ?? ''
        color.value = props.board.color || '#1FA6A0'
    } else {
        title.value = ''
        description.value = ''
        color.value = '#1FA6A0'
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
        if (isEditMode.value && props.board) {
            const payload: PatchedBoard = {
                title: title.value,
                description: description.value,
                color: color.value
            }
            await boardStore.updateBoard(props.board.slug, payload)
        } else {
            const payload: BoardPayload = {
                title: title.value,
                description: description.value,
                color: color.value
            }
            await boardStore.addBoard(payload)
        }
        modalInstance?.hide()
    } catch (e) {
        error.value = 'Failed to save board.'
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
                    <h5 class="modal-title">{{ isEditMode ? 'Edit board' : 'New board' }}</h5>
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
                        <div class="mb-3">
                            <label class="form-label">Color</label>
                            <input v-model="color" type="color" class="form-control form-control-color"
                                title="Choose board color" />
                        </div>
                        <div v-if="error" class="alert alert-danger py-2 mb-0">{{ error }}</div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary my-btn-outline-lift rounded-pill"
                            data-bs-dismiss="modal">
                            Cancel
                        </button>
                        <button type="submit" class="btn btn-primary my-btn-lift rounded-pill" :disabled="saving">
                            {{ isEditMode ? 'Save changes' : 'Create board' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>