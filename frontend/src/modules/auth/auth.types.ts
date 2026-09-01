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

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  first_name: string
  last_name: string
  email: string
  password: string
  password_confirm: string
}

export interface User {
  id: number
  first_name?: string
  last_name?: string
  email: string
  is_active: boolean
  is_superuser: boolean
  date_joined: string
}