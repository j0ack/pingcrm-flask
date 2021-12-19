<template>
  <button :disabled="loading" class="flex items-center">
    <div v-if="loading" class="btn-spinner mr-2" />
    <slot />
  </button>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

export default defineComponent({
  name: 'LoadingButton',
  props: {
    loading: {
      type: Boolean as PropType<boolean>,
      required: true
    }
  },
})
</script>
