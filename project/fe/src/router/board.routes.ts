import type { RouteRecordRaw } from 'vue-router'

export const boardRoutes: RouteRecordRaw[] = [
    {
        path: '/',
        name: 'boards',
        component: () => import('@/views/BoardListView.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/:slug',
        name: 'board-detail',
        component: () => import('@/views/BoardDetailView.vue'),
        meta: { requiresAuth: true }
    }
]