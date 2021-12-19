<template>
  <div>
    <h1 class="mb-8 font-bold text-3xl">Organizations</h1>
    <div class="mb-6 flex justify-between items-center">
      <search-filter :modelValue="form.search" class="w-full max-w-md mr-4" @reset="reset" @updateSearch="updateSearch">
        <label class="block text-gray-700">Trashed:</label>
        <select v-model="form.trashed" class="mt-1 w-full form-select">
          <option :value="null" />
          <option value="with">With Trashed</option>
          <option value="only">Only Trashed</option>
        </select>
      </search-filter>
      <Link class="btn-indigo" :href="$route('organization.create')">
        <span>Create Organization</span>
      </Link>
    </div>
    <div class="bg-white rounded-md shadow overflow-x-auto">
      <table class="w-full whitespace-nowrap">
        <thead>
          <tr class="text-left font-bold">
            <th class="px-6 pt-6 pb-4">Name</th>
            <th class="px-6 pt-6 pb-4">City</th>
            <th class="px-6 pt-6 pb-4" colspan="2">Phone</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="organization in organizations.data" :key="organization.id" class="hover:bg-gray-100 focus-within:bg-gray-100">
            <td class="border-t">
              <Link class="px-6 py-4 flex items-center focus:text-indigo-500" :href="$route('organization.edit', organization.id)">
                {{ organization.name }}
                <icon v-if="organization.deleted_at" name="trash" class="flex-shrink-0 w-3 h-3 fill-gray-400 ml-2" />
              </Link>
            </td>
            <td class="border-t">
              <Link class="px-6 py-4 flex items-center" :href="$route('organization.edit', organization.id)" tabindex="-1">
                {{ organization.city }}
              </Link>
            </td>
            <td class="border-t">
              <Link class="px-6 py-4 flex items-center" :href="$route('organization.edit', organization.id)" tabindex="-1">
                {{ organization.phone }}
              </Link>
            </td>
            <td class="border-t w-px">
              <Link class="px-4 flex items-center" :href="$route('organization.edit', organization.id)" tabindex="-1">
                <icon name="cheveron-right" class="block w-6 h-6 fill-gray-400" />
              </Link>
            </td>
          </tr>
          <tr v-if="organizations.data.length === 0">
            <td class="border-t px-6 py-4" colspan="4">No organizations found.</td>
          </tr>
        </tbody>
      </table>
    </div>
    <pagination class="mt-6" :links="organizations.links" />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import { Link as LinkModel, Organization, SearchFilters } from '@/models'
import { Link } from '@inertiajs/inertia-vue3'
import Icon from '@/common/Icon.vue'
import Layout from '@/common/Layout.vue'
import Pagination from '@/common/Pagination.vue'
import SearchFilter from '@/common/SearchFilter.vue'

type OrganizationSearch = {
  data: Organization[],
  links: LinkModel[],
}

export default defineComponent({
  metaInfo: { title: 'Organizations' },
  components: {
    Link,
    Icon,
    Pagination,
    SearchFilter,
  },
  layout: Layout,
  props: {
    organizations: {
      type: Object as PropType<OrganizationSearch>,
      required: true
    },
    filters: {
      type: Object as PropType<SearchFilters>,
      required: true
    }
  },
  data() {
    return {
      form: {
        search: this.filters.search,
        trashed: this.filters.trashed,
      },
    }
  },
  watch: {
    form: {
      handler(form) {
        let url = this.$route('organization.search')
        let params = []
        if (form.search) {
          params.push(`search=${form.search}`)
        }
        if (form.trashed) {
          params.push(`trashed=${form.trashed}`)
        }

        if (params) {
          url = `${url}?${params.join('&')}`
        }

        this.$inertia.get(url)
      },
      deep: true,
    },
  },
  methods: {
    reset() {
      this.form.search = ''
      this.form.trashed = ''
    },
    updateSearch(value: string) {
      this.form.search = value
    }
  },
})
</script>
