import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import ToastService from 'primevue/toastservice'
import './assets/main.css'
import 'primeicons/primeicons.css'
import ConfirmationService from 'primevue/confirmationservice'

import App from './app/App.vue'
import router from './app/router/index.js'

const savedTheme = localStorage.getItem('theme')

const isDark = savedTheme
  ? savedTheme === 'dark'
  : window.matchMedia('(prefers-color-scheme: dark)').matches

document.documentElement.classList.toggle('my-app-dark', isDark)

const app = createApp(App)
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: '.my-app-dark',
    },
  },
})

app.use(createPinia())
app.use(ConfirmationService)
app.use(ToastService)
app.use(router)

router.isReady().then(() => {
  app.mount('#app')
})
