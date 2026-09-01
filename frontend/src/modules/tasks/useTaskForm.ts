import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'

import {
  createTask,
  updateTask,
} from './tasks.api'

import type { Task } from './tasks.types'
import {parseApiErrors} from '@/shared/utils/parseApiErrors'

export const useTaskForm = (
  onSuccess: () => Promise<void>
) => {
  const toast = useToast()

  const visible = ref(false)
  const loading = ref(false)
  const isEditing = ref(false)
  const editingTaskId = ref<number | null>(null)
  const errors = ref<Record<string, string>>({})

  const formData = ref<Partial<Task>>({
    name: '',
    description: '',
    status: 'TODO',
    priority: 'MEDIUM',
    due_date: null,
  })

  const resetForm = () => {
    formData.value = {
      name: '',
      description: '',
      status: 'TODO',
      priority: 'MEDIUM',
      due_date: null,
    }

    errors.value = {}
    editingTaskId.value = null
    isEditing.value = false
  }

  const openCreate = () => {
    resetForm()
    visible.value = true
  }

  const openEdit = (task: Task) => {
    isEditing.value = true
    editingTaskId.value = task.id

    formData.value = {
      id: task.id,
      name: task.name,
      description: task.description,
      status: task.status,
      priority: task.priority,
      due_date: task.due_date,
    }

    errors.value = {}
    visible.value = true
  }

  const submit = async (task: Task) => {
    loading.value = true
    errors.value = {}

    const editing = isEditing.value

    try {
      if (editing && editingTaskId.value !== null) {
        await updateTask(
          editingTaskId.value,
          task
        )
      } else {
        await createTask(task)
      }

      visible.value = false

      toast.add({
        severity: 'success',
        summary: 'Success',
        detail: editing
          ? 'Task updated successfully'
          : 'Task created successfully',
        life: 3000,
      })

      resetForm()

      await onSuccess()

    } catch (err: unknown) {
      console.error('Failed to save task:', err)

      errors.value = parseApiErrors(err)

      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: editing
          ? 'Failed to update task'
          : 'Failed to create task',
        life: 3000,
      })

      // Keep throwing so the caller can still handle
      // the error if necessary.
      throw err

    } finally {
      loading.value = false
    }
  }

  return {
    visible,
    loading,
    isEditing,
    editingTaskId,
    errors,
    formData,
    resetForm,
    openCreate,
    openEdit,
    submit,
  }
}