export const statusOptions = [
  { label: 'To Do', value: 'TODO' },
  { label: 'In Progress', value: 'IN PROGRESS' },
  { label: 'Done', value: 'DONE' },
]

export const priorityOptions = [
  { label: 'Low', value: 'LOW' },
  { label: 'Medium', value: 'MEDIUM' },
  { label: 'High', value: 'HIGH' },
]

export interface Task {
  id?: number
  user?: number
  name?: string
  description?: string
  status: string
  priority: string
  due_date?: string | null
}

export interface TaskFilters {
  page?: number
  ordering?: string
  search?: string
  status?: string
  priority?: string
}
 

