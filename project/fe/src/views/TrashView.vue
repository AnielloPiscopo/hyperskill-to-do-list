<script setup lang="ts">
import ArchivedBoardsSection from '@/components/domain/board/ArchivedBoardsSection.vue'
import ArchivedTasksSection from '@/components/domain/task/ArchivedTasksSection.vue'
</script>

<template>
    <h1 class="h2 mb-4">Trash</h1>

    <section class="mb-4">
        <ArchivedBoardsSection />
    </section>

    <section>
        <ArchivedTasksSection />
    </section>
</template>