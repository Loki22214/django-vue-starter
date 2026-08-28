<script setup lang="ts">
import { ref, watch } from 'vue'

import Dialog from 'primevue/dialog'
import Label from 'primevue/label'
import Select from 'primevue/select'
import DatePicker from 'primevue/datepicker'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Message from 'primevue/message'

import type { Task } from './tasks.types'

const props = defineProps<{
  visible: boolean
  formData: Task
  errors: Record<string, string>
  statusOptions: { label: string; value: string }[]
  priorityOptions: { label: string; value: string }[]
  loadingCreate: boolean
  isEditing: boolean
}>()

const emit = defineEmits<{
  addTask: [task: Task]
  'update:visible': [value: boolean]
}>()

const localFormData = ref<Task>({
  ...props.formData,
})

watch(
  () => props.formData,
  (newFormData) => {
    localFormData.value = {
      ...newFormData,
    }
  },
  { deep: true },
)

const submit = () => {
  emit('addTask', localFormData.value)
}
</script>

<template>
  <div class="flex justify-center">
    <Dialog
      :visible="visible"
      modal
      :header="isEditing ? 'Edit Task' : 'Create Task'"
      :style="{ width: '24rem' }"
      @update:visible="emit('update:visible', $event)"
    >
      <div class="flex flex-col gap-4">
        <!-- Name -->
        <div class="flex flex-col gap-1.5">
          <Label for="name">
            Name
          </Label>

          <InputText
            id="name"
            v-model="localFormData.name"
            autofocus
            :invalid="!!errors.name"
          />

          <Message
            v-if="errors.name"
            severity="error"
            variant="simple"
          >
            {{ errors.name }}
          </Message>
        </div>

        <!-- Description -->
        <div class="flex flex-col gap-1.5">
          <Label for="description">
            Description
          </Label>

          <InputText
            id="description"
            v-model="localFormData.description"
            :invalid="!!errors.description"
          />

          <Message
            v-if="errors.description"
            severity="error"
            variant="simple"
          >
            {{ errors.description }}
          </Message>
        </div>

        <!-- Status -->
        <div class="flex flex-col gap-1.5">
          <Label for="status">
            Status
          </Label>

          <Select
            id="status"
            v-model="localFormData.status"
            :options="statusOptions"
            optionLabel="label"
            optionValue="value"
            :invalid="!!errors.status"
          />

          <Message
            v-if="errors.status"
            severity="error"
            variant="simple"
          >
            {{ errors.status }}
          </Message>
        </div>

        <!-- Priority -->
        <div class="flex flex-col gap-1.5">
          <Label for="priority">
            Priority
          </Label>

          <Select
            id="priority"
            v-model="localFormData.priority"
            :options="priorityOptions"
            optionLabel="label"
            optionValue="value"
            :invalid="!!errors.priority"
          />

          <Message
            v-if="errors.priority"
            severity="error"
            variant="simple"
          >
            {{ errors.priority }}
          </Message>
        </div>

        <!-- Due Date -->
        <div class="flex flex-col gap-1.5">
          <Label for="due_date">
            Due Date
          </Label>

          <DatePicker
            v-model="localFormData.due_date"
            dateFormat="yy-mm-dd"
            updateModelType="string"
            showIcon
            fluid
            iconDisplay="input"
            inputId="due_date"
            :invalid="!!errors.due_date"
          />

          <Message
            v-if="errors.due_date"
            severity="error"
            variant="simple"
          >
            {{ errors.due_date }}
          </Message>
        </div>
      </div>

      <template #footer>
        <Button
          severity="secondary"
          variant="outlined"
          :disabled="loadingCreate"
          @click="emit('update:visible', false)"
        >
          Cancel
        </Button>

        <Button
          type="button"
          :disabled="loadingCreate"
          @click="submit"
        >
          <i
            v-if="loadingCreate"
            class="pi pi-spin pi-spinner"
          />

          <i
            v-else
            class="pi pi-check"
          />

          {{ loadingCreate ? 'Saving...' : isEditing ? 'Save Changes' : 'Save' }}
        </Button>
      </template>
    </Dialog>
  </div>
</template>