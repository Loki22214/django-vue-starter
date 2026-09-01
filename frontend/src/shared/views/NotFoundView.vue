<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center">
      <h1 class="text-8xl font-bold text-gray-800 mb-2">404</h1>

      <h2 class="text-2xl font-medium text-gray-600 mb-6">Oops! Page not found</h2>

      <Button label="Return Home" icon="pi pi-home" @click="router.push('/dashboard')" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import Button from 'primevue/button'

const router = useRouter()
</script>
