import axios, { AxiosError, type AxiosInstance, type InternalAxiosRequestConfig } from 'axios'

const client: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  withCredentials: true,
  timeout: 10000, // 10 seconds
  headers: {
    'Content-Type': 'application/json',
  },
})

// Prevent infinite refresh loops
let isRefreshing = false

let failedQueue: Array<{
  resolve: () => void
  reject: (error: unknown) => void
}> = []

const processQueue = (error?: unknown) => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error)
    } else {
      resolve()
    }
  })

  failedQueue = []
}

// Request interceptor
client.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    return config
  },
  (error) => Promise.reject(error),
)

// Response interceptor
client.interceptors.response.use(
  (response) => response,

  async (error: AxiosError) => {
    const originalRequest = error.config as
      (InternalAxiosRequestConfig & { _retry?: boolean }) | undefined

    if (!originalRequest) {
      return Promise.reject(error)
    }

    // Only handle expired access tokens
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }

    // Don't refresh the refresh endpoint itself
    if (originalRequest.url?.includes('/auth/refresh/')) {
      return Promise.reject(error)
    }

    originalRequest._retry = true

    if (isRefreshing) {
      return new Promise<void>((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      }).then(() => client(originalRequest))
    }

    isRefreshing = true

    try {
      // Refresh the access token using the refresh token
      await client.post('/auth/refresh/')

      processQueue()

      return client(originalRequest)
    } catch (refreshError) {
      processQueue(refreshError)

      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  },
)

export default client
