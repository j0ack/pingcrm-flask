<template>
  <div>
    <div class="mb-4">
      <Link class="flex items-center group py-3" :href="$route('dashboard')">
        <icon name="dashboard" class="w-4 h-4 mr-2 fill-white" />
        <div class="text-white">Dashboard</div>
      </Link>
    </div>
    <div class="mb-4">
      <Link class="flex items-center group py-3" :href="$route('organization.search')">
        <icon name="office" class="w-4 h-4 mr-2 fill-white" />
        <div class="text-white">Organizations</div>
      </Link>
    </div>
    <div class="mb-4">
      <Link class="flex items-center group py-3" :href="$route('contacts.search')">
        <icon name="users" class="w-4 h-4 mr-2 fill-white" />
        <div class="text-white">Contacts</div>
      </Link>
    </div>
    <div class="mb-4">
      <Link class="flex items-center group py-3" :href="$route('dashboard')">
        <icon name="printer" class="w-4 h-4 mr-2 fill-white" />
        <div class="text-white">Reports</div>
      </Link>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { Link } from '@inertiajs/inertia-vue3'
import Icon from '@/common/Icon.vue'

export default defineComponent({
  name: 'MainMenu',
  components: {
    Link,
    Icon,
  }
})
</script>
