import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '@/modules/auth/LoginView.vue'
import RegisterView from '@/modules/auth/RegisterView.vue'
import DashboardView from '@/modules/dashboard/DashboardView.vue'
import TaskView from '@/modules/tasks/TasksView.vue'
import NotFoundView from '@/shared/NotFoundView.vue'
import { useAuthStore } from '@/modules/auth/auth.store'

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: TaskView,
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView,
    },
  ],
})

let authInitialized = false
router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (!authInitialized) {
    try {
      await authStore.fetchUser()
    } catch {
      // No valid session
    } finally {
      authInitialized = true
    }
  }

  const isLoggedIn = authStore.isAuthenticated
  if (to.path === '/') {
    return {
      name: isLoggedIn ? 'dashboard' : 'login',
    }
  }

  if (to.meta.requiresAuth && !isLoggedIn) {
    return { name: 'login' }
  }

  if (to.name === 'login' && isLoggedIn) {
    return { name: 'dashboard' }
  }
})

export default router
