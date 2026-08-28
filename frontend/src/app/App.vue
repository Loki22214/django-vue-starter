<script setup lang="ts">
import DefaultLayout from '@/app/layouts/DefaultLayout.vue'
import { useRoute } from 'vue-router'
import Toast from 'primevue/toast'

const route = useRoute()
</script>

<template>
  <Toast position="top-right" />
  <RouterView
    v-if="route.name === 'login' || route.name === 'not-found' || route.name === 'register'"
  />

  <DefaultLayout v-else>
    <router-view />
  </DefaultLayout>
</template>

<style scoped></style>
