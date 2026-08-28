<script setup lang="ts">
import { ref, watch } from 'vue'
import type { TaskFilters } from './tasks.types'
import { statusOptions, priorityOptions } from './tasks.types'

import Dialog from 'primevue/dialog'
import Select from 'primevue/select'
import Button from 'primevue/button'

const props = defineProps<{
    visible: boolean
    filters: TaskFilters
}>()

const emit = defineEmits<{
    'update:visible': [value: boolean]
    apply: [filters: Pick<TaskFilters, 'status' | 'priority'>]
}>()

const localFilters = ref({
    status: props.filters.status,
    priority: props.filters.priority,
})

watch(
    () => props.visible,
    (visible) => {
        if (visible) {
            localFilters.value = {
                status: props.filters.status,
                priority: props.filters.priority,
            }
        }
    }
)

const close = () => {
    emit('update:visible', false)
}

const apply = () => {
    emit('apply', {
        status: localFilters.value.status,
        priority: localFilters.value.priority,
    })

    close()
}

const clear = () => {
    localFilters.value = {
        status: '',
        priority: '',
    }
}
</script>

<template>
    <Dialog :visible="visible" modal header="Filter tasks" :style="{ width: '24rem' }"
        @update:visible="emit('update:visible', $event)">
        <div class="flex flex-col gap-4">

            <div class="flex flex-col gap-1.5">
                <label for="status" class="font-medium">
                    Status
                </label>

                <Select id="status" v-model="localFilters.status" :options="statusOptions" optionLabel="label"
                    optionValue="value" placeholder="All statuses" showClear class="w-full" />
            </div>

            <div class="flex flex-col gap-1.5">
                <label for="priority" class="font-medium">
                    Priority
                </label>

                <Select id="priority" v-model="localFilters.priority" :options="priorityOptions" optionLabel="label"
                    optionValue="value" placeholder="All priorities" showClear class="w-full" />
            </div>

        </div>

        <template #footer>
            <Button label="Cancel" severity="secondary" text @click="close" />
            <div class="flex gap-2">
                <Button label="Reset" severity="secondary" variant="outlined" @click="clear" />


                <Button label="Apply" @click="apply" />
            </div>
        </template>
    </Dialog>
</template>