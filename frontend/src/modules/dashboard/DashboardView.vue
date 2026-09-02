<template>
  <div class="mx-auto max-w-6xl space-y-8">
    <section
      class="relative overflow-hidden rounded-2xl border border-primary-200 bg-primary-50 px-6 py-8 dark:border-primary-900 dark:bg-primary-950/40 sm:px-10 sm:py-10"
    >
      <div class="relative z-10 max-w-2xl">
        <p class="mb-3 text-sm font-semibold uppercase tracking-widest text-primary-600 dark:text-primary-300">
          Setup complete
        </p>
        <h1 class="m-0 text-3xl font-bold tracking-tight text-surface-900 dark:text-surface-0 sm:text-4xl">
          Welcome to your Django Vue app
        </h1>
        <p class="mt-4 mb-0 max-w-xl text-base leading-7 text-surface-600 dark:text-surface-300">
          Your foundation is ready. Follow the next steps to turn this template into your
          own product.
        </p>
      </div>
      <div
        class="pointer-events-none absolute -right-16 -bottom-24 size-72 rounded-full border-[24px] border-primary-200/70 dark:border-primary-800/50"
        aria-hidden="true"
      />
    </section>

    <section>
      <div class="mb-5">
        <p class="mb-1 text-sm font-semibold uppercase tracking-widest text-primary-600 dark:text-primary-300">
          Next steps
        </p>
        <h2 class="m-0 text-2xl font-bold text-surface-900 dark:text-surface-0">
          Make the template yours
        </h2>
        <p class="mt-2 mb-0 text-surface-600 dark:text-surface-300">
          A short path from starter project to your first feature.
        </p>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <article
          v-for="(step, index) in [
            {
              icon: 'pi-trash',
              title: 'Remove the demo Tasks app',
              description: 'Delete the example CRUD module, routes, migrations, and frontend task views when you are ready to start fresh.',
            },
            {
              icon: 'pi-sitemap',
              title: 'Extend the Django API',
              description: 'Create your domain app with models, serializers, views, URLs, permissions, and tests.',
            },
            {
              icon: 'pi-desktop',
              title: 'Build your frontend workflow',
              description: 'Replace this dashboard and add Vue views, stores, API clients, and reusable components for your product.',
            },
            {
              icon: 'pi-shield',
              title: 'Prepare for production',
              description: 'Set production environment values, review authentication and permissions, and run the test and lint checks.',
            },
          ]"
          :key="step.title"
          class="border border-surface-200 bg-surface-0 p-5 dark:border-surface-700 dark:bg-surface-900"
        >
          <div class="mb-5 flex items-center justify-between">
            <div class="flex size-10 items-center justify-center rounded-xl bg-primary-100 text-primary-600 dark:bg-primary-900/70 dark:text-primary-300">
              <i :class="['pi', step.icon]" aria-hidden="true" />
            </div>
            <span class="text-sm font-semibold text-surface-400 dark:text-surface-500">
              0{{ index + 1 }}
            </span>
          </div>
          <h3 class="m-0 text-lg font-semibold text-surface-900 dark:text-surface-0">
            {{ step.title }}
          </h3>
          <p class="mt-2 mb-0 text-sm leading-6 text-surface-600 dark:text-surface-300">
            {{ step.description }}
          </p>
        </article>
      </div>
    </section>

    <section
      class="flex flex-col gap-4 border border-surface-200 bg-surface-0 p-5 dark:border-surface-700 dark:bg-surface-900 sm:flex-row sm:items-center sm:justify-between"
    >
      <div>
        <h2 class="m-0 text-lg font-semibold text-surface-900 dark:text-surface-0">
          Need to inspect the API?
        </h2>
        <p class="mt-1 mb-0 text-sm text-surface-600 dark:text-surface-300">
          Open the interactive Swagger documentation while you build your first endpoint.
        </p>
      </div>
      <a
        href="http://localhost:8000/api/docs/"
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex shrink-0 items-center justify-center gap-2 rounded-lg border border-surface-300 px-4 py-2.5 text-sm font-semibold text-surface-700 no-underline transition-colors hover:bg-surface-100 dark:border-surface-600 dark:text-surface-200 dark:hover:bg-surface-800"
      >
        Open API docs
        <i class="pi pi-external-link text-xs" aria-hidden="true" />
      </a>
    </section>
  </div>
</template>
