import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { authRoutes } from './auth.routes'
import { boardRoutes } from './board.routes'
import { appRoutes } from './app.routes'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...authRoutes, ...boardRoutes, ...appRoutes]
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) return { name: 'login' }
  if (to.meta.guest && authStore.isAuthenticated) return { name: 'boards' }
})

export default router
