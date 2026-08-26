<script setup lang="ts">
import type { Task } from '@/types'

const props = defineProps<{ task: Task; archived?: boolean }>()
const emit = defineEmits<{ select: [task: Task]; archive: [id: number] }>()

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
        <div>
            <span class="fw-medium">{{ task.title }}</span>
            <span v-if="!archived" class="badge rounded-pill ms-2 my-text-mono" :class="{
                'text-bg-light border': task.status === 'TODO',
                'text-bg-info': task.status === 'IN_PROGRESS',
                'text-bg-success': task.status === 'DONE'
            }">
                {{ task.status }}
            </span>
        </div>
        <button v-if="!archived" class="btn btn-sm btn-outline-secondary rounded-pill"
            @click.stop="emit('archive', task.id)">
            Archive
        </button>
    </article>
</template>