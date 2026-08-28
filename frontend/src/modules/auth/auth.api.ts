import client from '../../app/client'

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
  first_name: string
  last_name: string
  email: string
}

export const login = async (payload: LoginPayload) => {
  const response = await client.post('/auth/login/', payload)
  return response.data
}

export const logout = async () => {
  const response = await client.post('/auth/logout/')
  return response.data
}

export const register = async (payload: RegisterPayload) => {
  const response = await client.post('/auth/register/', payload)
  return response.data
}

export const getCurrentUser = async (): Promise<User> => {
  const response = await client.get<User>('/auth/me/')
  return response.data
}

export const refreshToken = async () => {
  const response = await client.post('/auth/refresh/')
  return response.data
}
