<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './auth.store'

import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Label from 'primevue/label'
import Message from 'primevue/message'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
  rememberMe: false,
})

const login = async () => {
  try {
    await authStore.login(form)
    router.push('/dashboard')
  } catch {
    // Error is handled through authStore.error
  }
}

const goToForgotPassword = () => {
  router.push('/forgot-password')
}

const goToCreateAccount = () => {
  router.push('/register')
}

onMounted(() => {
  authStore.clearErrors()
})
</script>

<template>
  <div class="flex justify-center items-center min-h-screen p-4">
    <Card class="max-w-md w-full p-6">
      <template #title>
        <div class="text-center text-3xl font-bold">Welcome back</div>
      </template>

      <template #subtitle>
        <div class="text-center text-surface-500">Sign in with your email to continue.</div>
      </template>

      <template #content>
        <form class="flex flex-col gap-5 mt-5" @submit.prevent="login">
          <div class="flex flex-col gap-2">
            <Label for="email">Email</Label>

            <InputText
              id="email"
              v-model="form.email"
              type="email"
              autocomplete="email"
              class="w-full"
              :invalid="!!authStore.fieldErrors.email"
            />
            <Message
              v-if="authStore.fieldErrors.email"
              severity="error"
              size="small"
              variant="simple"
            >
              {{ authStore.fieldErrors.email[0] }}
            </Message>
          </div>

          <div class="flex flex-col gap-2">
            <Label for="password">Password</Label>

            <InputText
              id="password"
              v-model="form.password"
              type="password"
              autocomplete="current-password"
              class="w-full"
              :invalid="!!authStore.fieldErrors.password"
            />
            <Message
              v-if="authStore.fieldErrors.password"
              severity="error"
              size="small"
              variant="simple"
            >
              {{ authStore.fieldErrors.password[0] }}
            </Message>
          </div>

          <!-- Remember me + Forgot password -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <Checkbox id="remember" v-model="form.rememberMe" binary />

              <Label for="remember"> Remember me </Label>
            </div>

            <Button
              type="button"
              label="Forgot password?"
              variant="link"
              class="p-0"
              @click="goToForgotPassword"
            />
          </div>

          <Message v-if="authStore.error" severity="error" size="small" closable>
            {{ authStore.error }}
          </Message>

          <!-- Login button -->
          <Button
            type="submit"
            label="Login"
            class="w-full"
            :loading="authStore.loading"
            :disabled="authStore.loading"
          />
        </form>
      </template>

      <template #footer>
        <div class="text-center text-surface-500 text-sm mt-1">
          Don't have an account?

          <Button
            type="button"
            label="Sign up"
            variant="link"
            class="p-0"
            @click="goToCreateAccount"
          />
        </div>
      </template>
    </Card>
  </div>
</template>
