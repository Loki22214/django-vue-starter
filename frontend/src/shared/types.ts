export interface ApiErrorResponse {
  success?: boolean
  code?: number
  message?: string
  errors?: {
    [key: string]: string | string[]
  }
}
