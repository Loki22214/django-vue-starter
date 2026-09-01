export interface ApiErrorResponse {
  success?: boolean
  code?: number
  message?: string
  errors?: {
    [key: string]: string | string[]
  }
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}