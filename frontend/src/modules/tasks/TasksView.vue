<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useConfirm } from 'primevue/useconfirm'

import Button from 'primevue/button'
import ConfirmDialog from 'primevue/confirmdialog'

import TaskCreateModal from '@/modules/tasks/TaskCreateModal.vue'
import TaskDataTable from '@/modules/tasks/TaskDataTable.vue'
import TasksFilter from '@/modules/tasks/TaskFilterModal.vue'

import {
  statusOptions,
  priorityOptions,
  type Task,
} from '@/modules/tasks/tasks.types'

import { useTasks } from '@/modules/tasks/useTasks'
import { useTaskForm } from '@/modules/tasks/useTaskForm'

const confirm = useConfirm()

const filterVisible = ref(false)

const {
  tasks,
  loading,
  filters,
  totalRecords,
  hasActiveFilters,
  fetchTasks,
  applyFilters,
  clearFilters,
  onSort,
  onPage,
  deleteTask,
} = useTasks()

const {
  visible,
  loading: loadingCreate,
  isEditing,
  errors: formErrors,
  formData,
  openCreate,
  openEdit,
  submit,
} = useTaskForm(fetchTasks)

/**
 * Delete task confirmation
 */
const confirmDelete = (task: Task) => {
  confirm.require({
    message: `Are you sure you want to delete "${task.name}"?`,
    header: 'Delete Task',
    icon: 'pi pi-exclamation-triangle',

    rejectLabel: 'Cancel',
    rejectProps: {
      label: 'Cancel',
      severity: 'secondary',
      outlined: true,
    },

    acceptProps: {
      label: 'Delete',
      severity: 'danger',
    },

    accept: () => {
      if (task.id !== undefined) {
        deleteTask(task.id)
      }
    },
  })
}

onMounted(() => {
  fetchTasks()
})
</script>

<template>
  <div class="tasks-page">
    <!-- Confirmation dialog -->
    <ConfirmDialog />

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-3xl font-bold m-0">
          Tasks
        </h1>

        <p class="text-muted-color text-sm mt-2 mb-0">
          Keep track of your work in one place.
        </p>
      </div>

      <Button
        label="Add New"
        icon="pi pi-plus"
        @click="openCreate"
      />
    </div>

    <!-- Tasks table -->
    <div>
      <TaskDataTable
        :tasks="tasks"
        :loading="loading"
        :filters="filters"
        :total-records="totalRecords"
        :has-active-filters="hasActiveFilters"
        @update:search="filters.search = $event"
        @toggle-filter="filterVisible = true"
        @clear-filters="clearFilters"
        @page="onPage"
        @sort="onSort"
        @edit-task="openEdit"
        @delete-task="confirmDelete"
      />
    </div>
  </div>

  <!-- Create / Edit modal -->
  <TaskCreateModal
    v-model:visible="visible"
    :formData="formData"
    :errors="formErrors"
    :statusOptions="statusOptions"
    :priorityOptions="priorityOptions"
    :loadingCreate="loadingCreate"
    :isEditing="isEditing"
    @addTask="submit"
  />

  <!-- Filter modal -->
  <TasksFilter
    v-model:visible="filterVisible"
    :filters="filters"
    @apply="applyFilters"
  />
</template>