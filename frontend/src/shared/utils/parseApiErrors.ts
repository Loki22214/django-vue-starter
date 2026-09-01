export interface ApiErrorResponse {
  errors?: Record<string, string | string[]>
}

export function parseApiErrors(err: unknown): Record<string, string> {
  const response = (
    err as {
      response?: {
        data?: ApiErrorResponse
      }
    }
  ).response

  const apiErrors = response?.data?.errors

  if (!apiErrors) {
    return {}
  }

  const errors: Record<string, string> = {}

  for (const key in apiErrors) {
    const value = apiErrors[key]

    errors[key] = Array.isArray(value)
      ? value.join(', ')
      : String(value)
  }

  return errors
}