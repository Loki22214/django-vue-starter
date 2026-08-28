import client from '../../app/client'
import type { Task, TaskFilters } from './tasks.types'

export interface PaginatedTasks {
  count: number
  next: string | null
  previous: string | null
  results: Task[]
}

export const getTasks = async (filters: TaskFilters): Promise<PaginatedTasks> => {
  const response = await client.get('/tasks', { params: filters })
  return response.data.data
}

export const getTask = async (task_id: number): Promise<Task> => {
  const response = await client.get(`/tasks/${task_id}/`)
  return response.data
}

export const createTask = async (payload: Task): Promise<Task> => {
  const response = await client.post<Task>('/tasks/', payload)
  return response.data
}

export const updateTask = async (task_id: number, payload: Partial<Task>): Promise<Task> => {
  const response = await client.put(`/tasks/${task_id}/`, payload)
  return response.data
}

export const deleteTask = async (task_id: number) => {
  const response = await client.delete(`/tasks/${task_id}/`)
  return response.data
}
