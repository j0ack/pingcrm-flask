<template>
  <h1 class="mb-8 font-bold text-3xl">
    <Link class="text-indigo-400 hover:text-indigo-600" :href="$route('organization.search')">Organizations</Link>
    <span class="text-indigo-400 font-medium">/</span> Create
  </h1>
  <div class="bg-white rounded-md shadow overflow-hidden max-w-3xl">
    <form @submit.prevent="store">
      <div class="p-8 -mr-6 -mb-8 flex flex-wrap">
        <text-input v-model="form.name" :error="form.errors.name" class="pr-6 pb-8 w-full lg:w-1/2" label="Name" />
        <text-input v-model="form.email" :error="form.errors.email" class="pr-6 pb-8 w-full lg:w-1/2" label="Email" />
        <text-input v-model="form.phone" :error="form.errors.phone" class="pr-6 pb-8 w-full lg:w-1/2" label="Phone" />
        <text-input v-model="form.address" :error="form.errors.address" class="pr-6 pb-8 w-full lg:w-1/2" label="Address" />
        <text-input v-model="form.city" :error="form.errors.city" class="pr-6 pb-8 w-full lg:w-1/2" label="City" />
        <text-input v-model="form.region" :error="form.errors.region" class="pr-6 pb-8 w-full lg:w-1/2" label="Province/State" />
        <select-input v-model="form.country" :error="form.errors.country" class="pr-6 pb-8 w-full lg:w-1/2" label="Country">
          <option :value="null" />
          <option value="CA">Canada</option>
          <option value="US">United States</option>
        </select-input>
        <text-input :value ="form.postal_code" :error="form.errors.postal_code" class="pr-6 pb-8 w-full lg:w-1/2" label="Postal code" />
      </div>
      <div class="px-8 py-4 bg-gray-50 border-t border-gray-100 flex justify-end items-center">
        <loading-button :loading="form.processing" class="btn-indigo" type="submit">Create Organization</loading-button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { Link, useForm } from '@inertiajs/inertia-vue3'
import Layout from '@/common/Layout.vue'
import TextInput from '@/common/TextInput.vue'
import SelectInput from '@/common/SelectInput.vue'
import LoadingButton from '@/common/LoadingButton.vue'

export default defineComponent({
  metaInfo: { title: 'Create Organization' },
  components: {
    Link,
    LoadingButton,
    SelectInput,
    TextInput,
  },
  layout: Layout,
  data() {
    return {
      form: useForm({
        name: null,
        email: null,
        phone: null,
        address: null,
        city: null,
        region: null,
        country: null,
        postal_code: null,
      }),
    }
  },
  methods: {
    store() {
      this.form.post(this.$route('organization.create'))
    },
  },
})
</script>
