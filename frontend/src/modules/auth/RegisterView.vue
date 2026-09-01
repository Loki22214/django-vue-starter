<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from './auth.store'

import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import InputPassword from 'primevue/inputpassword'
import Button from 'primevue/button'
import Message from 'primevue/message'
import Label from 'primevue/label'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  password_confirm: '',
})

const showSuccessToast = () => {
  toast.add({
    severity: 'success',
    summary: 'Account created',
    detail: 'Your account has been created successfully. Please log in.',
    life: 3000,
  })
}
const register = async () => {
  try {
    await authStore.register(form)
    showSuccessToast()
    router.push('/login')
  } catch {
    // Error is handled through authStore.error
  }
}

const goToLogin = () => {
  router.push('/login')
}

onMounted(() => {
  authStore.clearErrors()
})
</script>

<template>
  <div class="flex justify-center items-center min-h-screen p-4">
    <Card class="max-w-lg w-full p-6">
      <template #title>
        <div class="text-center text-3xl font-bold">Create account</div>
      </template>

      <template #subtitle>
        <div class="text-center text-surface-500">Sign up to get started.</div>
      </template>

      <template #content>
        <form class="flex flex-col gap-5 mt-5" @submit.prevent="register">
          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-2">
              <Label for="first_name">First name</Label>
              <InputText
                id="first_name"
                v-model="form.first_name"
                type="text"
                autocomplete="given-name"
                class="w-full"
                :invalid="!!authStore.fieldErrors.first_name"
                required
              />
              <Message
                v-if="authStore.fieldErrors.first_name"
                severity="error"
                size="small"
                variant="simple"
              >
                {{ authStore.fieldErrors.first_name[0] }}
              </Message>
            </div>

            <div class="flex flex-col gap-2">
              <Label for="last_name">Last name</Label>
              <InputText
                id="last_name"
                v-model="form.last_name"
                type="text"
                autocomplete="family-name"
                class="w-full"
                :invalid="!!authStore.fieldErrors.last_name"
                required
              />
              <Message
                v-if="authStore.fieldErrors.last_name"
                severity="error"
                size="small"
                variant="simple"
              >
                {{ authStore.fieldErrors.last_name[0] }}
              </Message>
            </div>
          </div>

          <div class="flex flex-col gap-2">
            <Label for="email">Email</Label>
            <InputText
              id="email"
              v-model="form.email"
              type="email"
              autocomplete="email"
              class="w-full"
              :invalid="!!authStore.fieldErrors.email"
              required
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
            <InputPassword
              input-id="password"
              v-model="form.password"
              :feedback="false"
              toggle-mask
              autocomplete="new-password"
              class="w-full"
              :invalid="!!authStore.fieldErrors.password"
              fluid
              required
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

          <div class="flex flex-col gap-2">
            <Label for="password_confirm"> Confirm password </Label>
            <InputPassword
              input-id="password_confirm"
              v-model="form.password_confirm"
              :feedback="false"
              toggle-mask
              autocomplete="new-password"
              class="w-full"
              :invalid="!!authStore.fieldErrors.password_confirm"
              fluid
              required
            />
            <Message
              v-if="authStore.fieldErrors.password_confirm"
              severity="error"
              size="small"
              variant="simple"
            >
              {{ authStore.fieldErrors.password_confirm[0] }}
            </Message>
          </div>

          <Message v-if="authStore.error" severity="error" size="small" closable>
            {{ authStore.error }}
          </Message>

          <Button
            type="submit"
            label="Create account"
            class="w-full"
            :loading="authStore.loading"
            :disabled="authStore.loading"
          />
        </form>
      </template>

      <template #footer>
        <div class="text-center text-surface-500 text-sm mt-1">
          Already have an account?

          <Button type="button" label="Sign in" variant="link" class="p-0" @click="goToLogin" />
        </div>
      </template>
    </Card>
  </div>
</template>
