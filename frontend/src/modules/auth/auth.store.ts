import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

import type { ApiErrorResponse } from '@/shared/types/types'
import type { User, LoginPayload, RegisterPayload } from './auth.types'
import client from '@/app/client'

interface FieldErrors {
  [key: string]: string[]
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)

  const loading = ref(false)

  // General error message
  const error = ref<string | null>(null)

  // Field-specific validation errors
  const fieldErrors = ref<FieldErrors>({})

  const isAuthenticated = ref(false)

  /**
   * Handle API errors consistently across login/register/etc.
   */
  const handleApiError = (err: unknown, fallbackMessage: string) => {
    error.value = null
    fieldErrors.value = {}

    if (!axios.isAxiosError<ApiErrorResponse>(err)) {
      error.value = fallbackMessage
      return
    }

    const data = err.response?.data

    if (!data) {
      error.value = fallbackMessage
      return
    }

    if (data.errors) {
      const errors: FieldErrors = {}

      for (const [field, messages] of Object.entries(data.errors)) {
        if (Array.isArray(messages)) {
          errors[field] = messages
        }
      }

      fieldErrors.value = errors

      const detail = data.errors.detail

      if (typeof detail === 'string') {
        error.value = detail
        return
      }

      if (Object.keys(errors).length > 0) {
        return
      }
    }

    // Fallback to top-level message
    error.value = data.message ?? fallbackMessage
  }

  const login = async (payload: LoginPayload) => {
    loading.value = true

    error.value = null
    fieldErrors.value = {}

    try {
      await client.post('/auth/login/', payload)

      await fetchUser()

      isAuthenticated.value = true
    } catch (err: unknown) {
      handleApiError(err, 'Login failed. Please check your credentials and try again.')

      isAuthenticated.value = false
      user.value = null

      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchUser = async () => {
    try {
      const response = await client.get<User>('/auth/me/')

      user.value = response.data
      isAuthenticated.value = true

      return response.data
    } catch (err) {
      user.value = null
      isAuthenticated.value = false

      throw err
    }
  }

  const logout = async () => {
    try {
      await client.post('/auth/logout/')
    } finally {
      user.value = null
      isAuthenticated.value = false
      error.value = null
      fieldErrors.value = {}
    }
  }

  const register = async (payload: RegisterPayload) => {
    loading.value = true

    error.value = null
    fieldErrors.value = {}

    try {
      await client.post('/auth/register/', payload)
    } catch (err: unknown) {
      handleApiError(err, 'Registracija nije uspješna.')

      throw err
    } finally {
      loading.value = false
    }
  }

  const clearErrors = () => {
    error.value = null
    fieldErrors.value = {}
  }

  return {
    user,
    loading,
    error,
    fieldErrors,
    isAuthenticated,
    
    clearErrors,
    login,
    logout,
    fetchUser,
    register,
  }
})
