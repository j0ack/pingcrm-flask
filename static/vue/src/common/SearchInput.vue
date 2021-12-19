<template>
  <div>
    <label v-if="label" class="form-label" :for="id">{{ label }}:</label>
    <select :id="id" ref="input" v-model="selected" v-bind="$attrs" class="form-select" :class="{ error: error }">
      <slot />
    </select>
    <div v-if="error" class="form-error">{{ error }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

export default defineComponent({
  name: 'SearchInput',
  inheritAttrs: false,
  props: {
    id: {
      type: String as PropType<string>,
      required: true
    },
    value: {
      type: [String, Number, Boolean] as PropType<string | number | boolean>,
      required: true
    },
    label: {
      type: String as PropType<string>,
      required: true
    },
    error: {
      type: String as PropType<string>
    }
  },
  data() {
    return {
      selected: this.value,
    }
  },
  watch: {
    selected(selected: string) {
      this.$emit('input', selected)
    },
  },
  methods: {
    focus() {
      (this.$refs.input as HTMLInputElement).focus()
    },
    select() {
      (this.$refs.input as HTMLInputElement).select()
    },
  },
})
</script>
