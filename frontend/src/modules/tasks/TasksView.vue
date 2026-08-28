<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useConfirm } from 'primevue/useconfirm'

import {
  statusOptions,
  priorityOptions,
} from '@/modules/tasks/tasks.types'

import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import Tag from 'primevue/tag'
import ConfirmDialog from 'primevue/confirmdialog'

import TaskCreateModal from '@/modules/tasks/TaskCreateModal.vue'
import TasksFilter from '@/modules/tasks/TaskFilterModal.vue'

import { useTasks } from '@/modules/tasks/useTasks'
import { useTaskForm } from '@/modules/tasks/useTaskForm'

import { Search, Inbox } from '@primeicons/vue'

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
 * Status
 */
const getStatusLabel = (value: string) => {
  return (
    statusOptions.find(
      (option) => option.value === value
    )?.label ?? value
  )
}

const getStatusSeverity = (value: string) => {
  switch (value) {
    case 'TODO':
      return 'secondary'
    case 'IN PROGRESS':
      return 'info'
    case 'DONE':
      return 'success'
    default:
      return undefined
  }
}

/**
 * Priority
 */
const getPriorityLabel = (value: string) => {
  return (
    priorityOptions.find(
      (option) => option.value === value
    )?.label ?? value
  )
}

const getPrioritySeverity = (value: string) => {
  switch (value) {
    case 'LOW':
      return 'success'
    case 'MEDIUM':
      return 'warn'
    case 'HIGH':
      return 'danger'
    default:
      return undefined
  }
}

/**
 * Delete task confirmation
 */
const confirmDelete = (task: { id: number; name: string }) => {
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
      deleteTask(task.id)
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
    <div
      class="
        border
        border-surface-200
        bg-surface-0
        dark:bg-surface-900
        dark:border-surface-700
        rounded-xl
        overflow-hidden
      "
    >
      <!-- Search / filters -->
      <div class="flex items-center justify-start gap-3 p-4">
        <IconField>
          <InputIcon>
            <Search />
          </InputIcon>

          <InputText
            v-model="filters.search"
            placeholder="Search tasks..."
          />
        </IconField>

        <!-- Open filters -->
        <Button
          icon="pi pi-filter"
          severity="secondary"
          rounded
          text
          aria-label="Filter tasks"
          @click="filterVisible = true"
        />

        <!-- Clear filters -->
        <Button
          v-if="hasActiveFilters"
          icon="pi pi-filter-slash"
          severity="secondary"
          rounded
          text
          aria-label="Clear filters"
          @click="clearFilters"
        />
      </div>

      <!-- Data table -->
      <DataTable
        :loading="loading"
        :value="tasks"
        paginator
        :rows="10"
        :totalRecords="totalRecords"
        lazy
        removable-sort
        @sort="onSort"
        @page="onPage"
      >
        <!-- Empty state -->
        <template #empty>
          <div
            class="
              flex
              flex-col
              items-center
              justify-center
              gap-3
              py-10
              text-center
            "
          >
            <div
              class="
                w-14
                h-14
                rounded-full
                bg-surface-100
                dark:bg-surface-800
                flex
                items-center
                justify-center
              "
            >
              <Inbox
                class="w-7 h-7 text-surface-400"
              />
            </div>

            <div>
              <p class="m-0 font-semibold">
                No tasks yet
              </p>

              <p class="mt-1 text-sm text-surface-500">
                Add your first task to see it listed here.
              </p>
            </div>
          </div>
        </template>

        <!-- Name -->
        <Column
          field="name"
          header="Name"
          sortable
        >
          <template #body="{ data }">
            <button
              type="button"
              class="
                text-bold
                hover:underline
                font-medium
                cursor-pointer
              "
              @click="openEdit(data)"
            >
              {{ data.name }}
            </button>
          </template>
        </Column>

        <!-- Description -->
        <Column
          field="description"
          header="Description"
        />

        <!-- Status -->
        <Column
          field="status"
          header="Status"
          sortable
        >
          <template #body="{ data }">
            <Tag
              :value="getStatusLabel(data.status)"
              :severity="getStatusSeverity(data.status)"
            />
          </template>
        </Column>

        <!-- Priority -->
        <Column
          field="priority"
          header="Priority"
          sortable
        >
          <template #body="{ data }">
            <Tag
              :value="getPriorityLabel(data.priority)"
              :severity="getPrioritySeverity(data.priority)"
            />
          </template>
        </Column>

        <!-- Due date -->
        <Column
          field="due_date"
          header="Due date"
          sortable
        />

        <!-- Actions -->
        <Column
          header="Actions"
          :exportable="false"
          style="width: 80px"
        >
          <template #body="{ data }">
            <Button
              icon="pi pi-trash"
              severity="danger"
              text
              rounded
              aria-label="Delete task"
              @click="confirmDelete(data)"
            />
          </template>
        </Column>

        <!-- Loading -->
        <template #loading>
          <div class="flex flex-col items-center gap-2">
            <i
              class="
                pi
                pi-spin
                pi-spinner
                text-2xl
                text-primary
              "
            />

            <span class="text-sm">
              Loading tasks…
            </span>
          </div>
        </template>
      </DataTable>
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