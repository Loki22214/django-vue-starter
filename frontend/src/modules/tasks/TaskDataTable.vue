<script setup lang="ts">
import Column from 'primevue/column'
import Button from 'primevue/button'
import Tag from 'primevue/tag'

import BaseDataTable from '@/shared/components/BaseDataTable.vue'
import {
  statusOptions,
  priorityOptions,
  type Task,
  type TaskFilters,
} from '@/modules/tasks/tasks.types'

interface Props {
  tasks: Task[]
  loading?: boolean
  filters: TaskFilters
  totalRecords?: number
  hasActiveFilters?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  totalRecords: 0,
  hasActiveFilters: false,
})

const emit = defineEmits<{
  'update:search': [value: string]
  'toggle-filter': []
  'clear-filters': []
  'page': [event: any]
  'sort': [event: any]
  'delete-task': [task: Task]
  'edit-task': [task: Task]
}>()

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
</script>

<template>
  <BaseDataTable
    :data="tasks"
    :loading="loading"
    :search-value="filters.search || ''"
    :total-records="totalRecords"
    :has-active-filters="hasActiveFilters"
    empty-state-icon="pi pi-inbox"
    empty-state-title="No tasks yet"
    empty-state-description="Add your first task to see it listed here."
    @update:search-value="emit('update:search', $event)"
    @toggle-filter="emit('toggle-filter')"
    @clear-filters="emit('clear-filters')"
    @page="emit('page', $event)"
    @sort="emit('sort', $event)"
  >
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
          @click="emit('edit-task', data)"
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
          @click="emit('delete-task', data)"
        />
      </template>
    </Column>
  </BaseDataTable>
</template>
