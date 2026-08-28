import { ref } from 'vue'

const STORAGE_KEY = 'theme'

const isDark = ref(document.documentElement.classList.contains('my-app-dark'))

const applyTheme = (dark: boolean) => {
  document.documentElement.classList.toggle('my-app-dark', dark)
  isDark.value = dark
  localStorage.setItem(STORAGE_KEY, dark ? 'dark' : 'light')
}

const initTheme = () => {
  const savedTheme = localStorage.getItem(STORAGE_KEY)

  if (savedTheme) {
    applyTheme(savedTheme === 'dark')
    return
  }

  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  document.documentElement.classList.toggle('my-app-dark', prefersDark)

  isDark.value = prefersDark
}

const toggleTheme = () => {
  applyTheme(!isDark.value)
}

export function useTheme() {
  return {
    isDark,
    initTheme,
    toggleTheme,
  }
}
