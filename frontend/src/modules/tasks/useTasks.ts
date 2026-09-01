import { computed, ref, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { useToast } from 'primevue/usetoast'

import { deleteTask as deleteTaskApi, getTasks } from './tasks.api'

import type {
  Task,
  TaskFilters,
} from './tasks.types'

export const useTasks = () => {
  const toast = useToast()

  const tasks = ref<Task[]>([])
  const loading = ref(false)
  const error = ref(false)
  const totalRecords = ref(0)

  const filters = ref<TaskFilters>({
    page: 1,
    ordering: '',
    search: '',
    status: '',
    priority: '',
  })

  const hasActiveFilters = computed(() => {
    return Boolean(
      filters.value.search ||
      filters.value.status ||
      filters.value.priority
    )
  })

  const fetchTasks = async () => {
    loading.value = true
    error.value = false

    try {
      const response = await getTasks(filters.value)

      tasks.value = response.results
      totalRecords.value = response.count
    } catch (err) {
      error.value = true

      console.error('Failed to fetch tasks:', err)

      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Failed to load tasks',
        life: 3000,
      })
    } finally {
      loading.value = false
    }
  }

  const deleteTask = async (taskId: number) => {
    try {
      await deleteTaskApi(taskId)

      // If the deleted task was the last item on the current page,
      // move back one page so the user doesn't end up on an empty page.
      if (tasks.value.length === 1 && (filters.value.page ?? 1) > 1) {
        filters.value.page = (filters.value.page ?? 1) - 1
      }

      await fetchTasks()

      toast.add({
        severity: 'success',
        summary: 'Success',
        detail: 'Task deleted successfully',
        life: 3000,
      })
    } catch (err) {
      console.error('Failed to delete task:', err)

      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Failed to delete task',
        life: 3000,
      })
    }
  }

  const searchTasks = useDebounceFn(() => {
    filters.value.page = 1
    fetchTasks()
  }, 300)

  watch(
    () => filters.value.search,
    () => {
      searchTasks()
    }
  )

  const applyFilters = (
    newFilters: Pick<TaskFilters, 'status' | 'priority'>
  ) => {
    filters.value.status = newFilters.status
    filters.value.priority = newFilters.priority
    filters.value.page = 1
    fetchTasks()
  }

  const clearFilters = () => {
    filters.value.search = ''
    filters.value.status = ''
    filters.value.priority = ''
    filters.value.page = 1
    fetchTasks()
  }

  const onSort = (event: {
    sortField?: string
    sortOrder?: number
  }) => {
    if (!event.sortField) {
      filters.value.ordering = ''
    } else {
      filters.value.ordering =
        event.sortOrder === -1
          ? `-${event.sortField}`
          : event.sortField
    }

    filters.value.page = 1
    fetchTasks()
  }

  const onPage = (event: {
    page: number
    first: number
    rows: number
  }) => {
    // PrimeVue page is zero-based.
    // Django pagination is usually one-based.
    filters.value.page = event.page + 1
    fetchTasks()
  }

  return {
    tasks,
    loading,
    error,
    filters,
    totalRecords,
    hasActiveFilters,
    fetchTasks,
    deleteTask,
    applyFilters,
    clearFilters,
    onSort,
    onPage,
  }
}