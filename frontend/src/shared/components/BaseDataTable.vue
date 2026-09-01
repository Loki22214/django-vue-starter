<script setup lang="ts" generic="T">
import { Search, Inbox } from '@primeicons/vue'

import DataTable from 'primevue/datatable'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'

interface Props<T> {
  data: T[]
  loading?: boolean
  totalRecords?: number
  searchValue?: string
  hasActiveFilters?: boolean
  emptyStateIcon?: string
  emptyStateTitle?: string
  emptyStateDescription?: string
}

const props = withDefaults(defineProps<Props<T>>(), {
  loading: false,
  totalRecords: 0,
  searchValue: '',
  hasActiveFilters: false,
  emptyStateIcon: 'pi pi-inbox',
  emptyStateTitle: 'No data yet',
  emptyStateDescription: 'Add your first item to see it listed here.',
})

const emit = defineEmits<{
  'update:searchValue': [value: string]
  'toggle-filter': []
  'clear-filters': []
  'page': [event: any]
  'sort': [event: any]
}>()

const handleSearchChange = (value: string | undefined) => {
  emit('update:searchValue', value ?? '')
}
</script>

<template>
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
          :model-value="searchValue"
          placeholder="Search..."
          @update:model-value="handleSearchChange"
        />
      </IconField>

      <!-- Open filters -->
      <Button
        icon="pi pi-filter"
        severity="secondary"
        rounded
        text
        aria-label="Filter"
        @click="emit('toggle-filter')"
      />

      <!-- Clear filters -->
      <Button
        v-if="hasActiveFilters"
        icon="pi pi-filter-slash"
        severity="secondary"
        rounded
        text
        aria-label="Clear filters"
        @click="emit('clear-filters')"
      />
    </div>

    <!-- Data table -->
    <DataTable
      :loading="loading"
      :value="data"
      paginator
      :rows="10"
      :totalRecords="totalRecords"
      lazy
      removable-sort
      @sort="emit('sort', $event)"
      @page="emit('page', $event)"
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
            <i :class="emptyStateIcon" class="w-7 h-7 text-surface-400" />
          </div>

          <div>
            <p class="m-0 font-semibold">
              {{ emptyStateTitle }}
            </p>

            <p class="mt-1 text-sm text-surface-500">
              {{ emptyStateDescription }}
            </p>
          </div>
        </div>
      </template>

      <!-- Columns slot -->
      <slot />

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
            Loading…
          </span>
        </div>
      </template>
    </DataTable>
  </div>
</template>
