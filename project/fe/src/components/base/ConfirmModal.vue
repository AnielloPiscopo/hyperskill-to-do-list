<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { Modal } from 'bootstrap'

const props = defineProps<{
    open: boolean
    title: string
    message: string
    confirmText?: string
    requireTypedConfirmation?: string
}>()
const emit = defineEmits<{ confirm: []; cancel: [] }>()

const modalRef = ref<HTMLElement | null>(null)
let modalInstance: Modal | null = null
const typedValue = ref('')

const canConfirm = computed(
    () => !props.requireTypedConfirmation || typedValue.value === props.requireTypedConfirmation
)

onMounted(() => {
    if (modalRef.value) {
        modalInstance = new Modal(modalRef.value)
        modalRef.value.addEventListener('hidden.bs.modal', () => emit('cancel'))
    }
})

watch(
    () => props.open,
    (open) => {
        if (open) {
            typedValue.value = ''
            modalInstance?.show()
        } else {
            modalInstance?.hide()
        }
    }
)

function handleConfirm() {
    emit('confirm')
    modalInstance?.hide()
}
</script>

<template>
    <div ref="modalRef" class="modal fade" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ title }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>{{ message }}</p>
                    <div v-if="requireTypedConfirmation">
                        <label class="form-label small text-muted">
                            Type <strong>{{ requireTypedConfirmation }}</strong> to confirm
                        </label>
                        <input v-model="typedValue" type="text" class="form-control" autocomplete="off" />
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary my-btn-outline-lift rounded-pill"
                        data-bs-dismiss="modal">
                        Cancel
                    </button>
                    <button type="button" class="btn btn-outline-danger my-btn-danger-lift rounded-pill"
                        :disabled="!canConfirm" @click="handleConfirm">
                        {{ confirmText || 'Confirm' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>