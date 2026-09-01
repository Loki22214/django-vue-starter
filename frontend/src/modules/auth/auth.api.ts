import client from '../../app/client'
import type { LoginPayload, RegisterPayload, User } from './auth.types'

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
