<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import Avatar from 'primevue/avatar'
import Button from 'primevue/button'

import Sidebar from 'primevue/sidebar'
import SidebarLayout from 'primevue/sidebarlayout'
import SidebarMain from 'primevue/sidebarmain'
import SidebarAside from 'primevue/sidebaraside'
import SidebarPanel from 'primevue/sidebarpanel'
import SidebarSpacer from 'primevue/sidebarspacer'
import SidebarHeader from 'primevue/sidebarheader'
import SidebarContent from 'primevue/sidebarcontent'
import SidebarFooter from 'primevue/sidebarfooter'
import SidebarGroup from 'primevue/sidebargroup'
import SidebarGroupContent from 'primevue/sidebargroupcontent'
import SidebarMenu from 'primevue/sidebarmenu'
import SidebarMenuItem from 'primevue/sidebarmenuitem'
import SidebarMenuButton from 'primevue/sidebarmenubutton'
import SidebarTrigger from 'primevue/sidebartrigger'
import SidebarIcon from '@primeicons/vue/sidebar'
import SidebarGroupLabel from 'primevue/sidebargrouplabel'
import SidebarBackdrop from 'primevue/sidebarbackdrop'
import Home from '@primeicons/vue/home'
import ListCheck from '@primeicons/vue/list-check'
import SignOut from '@primeicons/vue/sign-out'
import Moon from '@primeicons/vue/moon'
import Sun from '@primeicons/vue/sun'

import { useAuthStore } from '@/modules/auth/auth.store'
import { useTheme } from '@/shared/composables/useTheme'

const router = useRouter()
const authStore = useAuthStore()
const { initTheme, isDark, toggleTheme } = useTheme()

const isMobile = ref(false)
const sidebarOpen = ref(true)

let mediaQuery: MediaQueryList | null = null
let onMediaQueryChange: ((event: MediaQueryListEvent) => void) | null = null

const navigationItems = [
  {
    label: 'Home',
    icon: Home,
    to: '/dashboard',
  },
  {
    label: 'Tasks',
    icon: ListCheck,
    to: '/tasks',
  },
]

const logout = async () => {
  await authStore.logout()
  await router.push('/login')
}

onMounted(() => {
  initTheme()
  if (typeof window === 'undefined') {
    return
  }

  mediaQuery = window.matchMedia('(max-width: 1023px)')

  isMobile.value = mediaQuery.matches
  sidebarOpen.value = !mediaQuery.matches

  onMediaQueryChange = (event) => {
    isMobile.value = event.matches
    sidebarOpen.value = !event.matches
  }

  mediaQuery.addEventListener('change', onMediaQueryChange)
})

onBeforeUnmount(() => {
  if (mediaQuery && onMediaQueryChange) {
    mediaQuery.removeEventListener('change', onMediaQueryChange)
  }
})
</script>

<template>
  <SidebarLayout class="min-h-screen">
    <!-- Mobile backdrop -->
    <SidebarBackdrop v-if="isMobile && sidebarOpen" class="absolute!" />

    <!-- Sidebar -->
    <Sidebar
      id="main-sidebar"
      v-model:open="sidebarOpen"
      :collapsible="isMobile ? 'offcanvas' : 'icon'"
      :overlay="isMobile"
      width="15rem"
    >
      <SidebarSpacer />

      <SidebarAside>
        <SidebarPanel>
          <!-- Sidebar header -->
          <SidebarHeader>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton class="p-1!">
                  <div
                    class="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary text-primary-contrast text-xs font-bold"
                  >
                    DV
                  </div>
                  <span class="ml-2 text-sm font-semibold"> Django Vue Template </span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarHeader>

          <!-- Navigation -->
          <SidebarContent>
            <SidebarGroup>
               <SidebarGroupLabel>Navigation</SidebarGroupLabel>
              <SidebarGroupContent>
                <SidebarMenu>
                  <SidebarMenuItem v-for="item in navigationItems" :key="item.to">
                    <SidebarMenuButton
                      as="router-link"
                      :to="item.to"
                      :isActive="router.currentRoute.value.path === item.to"
                    >
                      <component :is="item.icon" class="shrink-0 size-4!" />

                      <span >
                        {{ item.label }}
                      </span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                </SidebarMenu>
              </SidebarGroupContent>
            </SidebarGroup>
          </SidebarContent>

          <!-- Sidebar footer -->
          <SidebarFooter>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton class="p-1!" @click="logout">
                  <SignOut />
                  <span> Sign out </span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarFooter>
        </SidebarPanel>
      </SidebarAside>
    </Sidebar>

    <!-- Main application area -->
    <SidebarMain>
      <!-- Navbar -->
      <header
        class="flex h-12 items-center gap-2 border-b dark:border-b-surface-700 border-b-surface-200 bg-surface-0 dark:bg-surface-900 px-4"
      >
        <!-- Sidebar collapse / open -->
        <SidebarTrigger severity="secondary" target="main-sidebar" :text="true" size="small">
          <SidebarIcon />
        </SidebarTrigger>

        <!-- Right side -->
        <div class="ml-auto flex items-center gap-1">
          <!-- Theme -->
          <Button
            severity="secondary"
            text
            rounded
            :icon="isDark ? undefined : undefined"
            aria-label="Toggle theme"
            @click="toggleTheme"
          >
            <Sun v-if="isDark" />

            <Moon v-else />
          </Button>
          <!-- Current user -->
          <Button severity="secondary" text rounded class="ml-1!" aria-label="Current user">
            <Avatar icon="pi pi-user" shape="circle" class="size-20" />
          </Button>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 p-6 dark:bg-[#0f0f11]"> 
        <slot />
      </main>
    </SidebarMain>
  </SidebarLayout>
</template>
