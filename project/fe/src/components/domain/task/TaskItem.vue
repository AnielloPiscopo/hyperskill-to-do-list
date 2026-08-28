<script setup lang="ts">
import type { Task } from '@/types'

defineProps<{ task: Task; archived?: boolean; selected?: boolean; boardArchived?: boolean }>()
const emit = defineEmits<{
    select: [task: Task]
    archive: [id: number]
    restore: [id: number]
    delete: [task: Task]
    toggleSelect: [id: number]
}>()

const priorityColor: Record<string, string> = {
    HIGH: 'var(--coral)',
    MEDIUM: 'var(--sun)',
    LOW: 'var(--teal)',
    ZERO: 'var(--paper-border)'
}
</script>

<template>
    <article
        class="my-task-row card p-3 d-flex flex-column flex-sm-row justify-content-between align-items-start align-items-sm-center gap-2"
        :style="!archived ? { '--priority-color': priorityColor[task.priority ?? 'ZERO'] } : {}" role="button"
        @click="emit('select', task)">
        <div class="d-flex align-items-center gap-2">
            <input v-if="archived" class="form-check-input" type="checkbox" :checked="selected" @click.stop
                @change="emit('toggleSelect', task.id)" />
            <span class="fw-medium">{{ task.title }}</span>
            <span v-if="!archived" class="badge rounded-pill ms-2 my-text-mono" :class="{
                'text-bg-light border': task.status === 'TODO',
                'text-bg-info': task.status === 'IN_PROGRESS',
                'text-bg-success': task.status === 'DONE'
            }">
                {{ task.status }}
            </span>
            <span v-if="archived && boardArchived" class="text-muted small ms-2"
                title="Restore the board first to bring this task back">
                (board archived)
            </span>
        </div>

        <div v-if="!archived">
            <button class="btn btn-sm btn-outline-secondary rounded-pill" @click.stop="emit('archive', task.id)">
                Archive
            </button>
        </div>
        <div v-else class="d-flex gap-2">
            <button class="btn btn-sm btn-outline-secondary my-btn-outline-lift rounded-pill" :disabled="boardArchived"
                @click.stop="emit('restore', task.id)">
                Restore
            </button>
            <button class="btn btn-sm btn-outline-danger my-btn-danger-lift rounded-pill"
                @click.stop="emit('delete', task)">
                Delete
            </button>
        </div>
    </article>
</template>