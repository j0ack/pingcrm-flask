<template>
  <div>
    <h1 class="mb-8 font-bold text-3xl">Dashboard</h1>
    <p class="mb-8 leading-normal">Hey there! Welcome to Ping CRM, a demo app designed to help illustrate how <a class="text-indigo-500 underline hover:text-orange-600" href="https://inertiajs.com">Inertia.js</a> works.</p>
    <div class="mb-8 flex">
      <Link class="btn-indigo" href="/500">500 error</Link>
      <Link class="btn-indigo ml-1" href="/404">404 error</Link>
    </div>
    <p class="leading-normal">👆 These links are intended to be broken to illustrate how error handling works with Inertia.js.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { Link } from '@inertiajs/inertia-vue3'
import Layout from '@/common/Layout.vue'

export default defineComponent({
  name: 'Dashboard',
  components: {
    Link,
  },
  layout: Layout
})
</script>
