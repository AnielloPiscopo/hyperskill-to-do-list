<script setup lang="ts">
import type { Board } from '@/types'

const props = defineProps<{
    board: Board
    archived?: boolean
    selectable?: boolean
    selected?: boolean
}>()
const emit = defineEmits<{
    edit: [board: Board]
    archive: [slug: string]
    restore: [slug: string]
    delete: [board: Board]
    toggleSelect: [id: number]
}>()
</script>

<template>
    <article class="card my-board-card h-100 p-3" :style="{ '--board-color': board.color || '#1FA6A0' }">
        <div class="d-flex align-items-start gap-2">
            <input v-if="selectable" class="form-check-input mt-1" type="checkbox" :checked="selected" @click.stop
                @change="emit('toggleSelect', board.id)" />
            <RouterLink :to="{ name: 'board-detail', params: { slug: board.slug } }"
                class="text-decoration-none text-reset flex-grow-1">
                <template v-if="archived">
                    <span class="fw-medium">{{ board.title }}</span>
                </template>
                <template v-else>
                    <h2 class="h5 mb-2">{{ board.title }}</h2>
                    <p class="text-muted small mb-0">{{ board.description || 'No description' }}</p>
                </template>
            </RouterLink>
        </div>

        <div class="d-flex gap-2 mt-3">
            <template v-if="archived">
                <button class="btn btn-sm btn-outline-secondary my-btn-outline-lift rounded-pill"
                    @click="emit('restore', board.slug)">
                    Restore
                </button>
                <button class="btn btn-sm btn-outline-danger my-btn-danger-lift rounded-pill"
                    @click="emit('delete', board)">
                    Delete
                </button>
            </template>
            <template v-else>
                <button class="btn btn-sm btn-outline-secondary my-btn-outline-lift rounded-pill"
                    @click="emit('edit', board)">
                    Edit
                </button>
                <button class="btn btn-sm btn-outline-secondary my-btn-outline-lift rounded-pill"
                    @click="emit('archive', board.slug)">
                    Archive
                </button>
            </template>
        </div>
    </article>
</template>

<style scoped>
.my-board-card {
    border-top: 5px solid var(--board-color, var(--teal));
    cursor: pointer;
}

.my-board-card:hover {
    transform: rotate(-0.6deg) translateY(-4px);
    box-shadow: 0 10px 22px rgba(43, 35, 32, 0.12);
}

@media (prefers-reduced-motion: reduce) {
    .my-board-card {
        transition: none !important;
    }
}
</style>