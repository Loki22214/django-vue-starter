export interface User {
  id: number
  email: string
  first_name?: string
  last_name?: string
  is_active: boolean
  is_superuser: boolean
  date_joined: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  user: User
}

export interface MeResponse {
  user: User
}

export interface ApiError {
  message: string
}
