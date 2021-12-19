<template>
  <div>
    <label v-if="label" class="form-label" :for="id">{{ label }}:</label>
    <input :id="id"
           ref="input"
           class="form-input"
           :class="{ error: error }"
           :type="type"
           :value="modelValue"
           @input="$emit('update:modelValue', $event.target.value)" />
    <div v-if="error" class="form-error">{{ error }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

export default defineComponent({
  name: 'TextInput',
  props: {
    id: {
      type: String as PropType<string>,
    },
    type: {
      type: String as PropType<string>,
      default: 'text',
    },
    modelValue: {
      type: String as PropType<string>,
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
  methods: {
    focus() {
      (this.$refs.input as HTMLInputElement).focus()
    },
    select() {
      (this.$refs.input as HTMLInputElement).select()
    },
    setSelectionRange(start: number, end: number) {
      (this.$refs.input as HTMLInputElement).setSelectionRange(start, end)
    },
  },
})
</script>
