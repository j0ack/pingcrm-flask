<template>
  <div>
    <label v-if="label" class="form-label" :for="id">{{ label }}:</label>
    <select :id="id" ref="input" v-model="selected" class="form-select" :class="{ error: error }">
      <slot />
    </select>
    <div v-if="error" class="form-error">{{ error }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

export default defineComponent({
  name: 'SelectInput',
  props: {
    id: {
      type: String as PropType<string>,
    },
    modelValue: {
      type: [String, Number, Boolean] as PropType<string | number | boolean>,
      required: true
    },
    label: {
      type: String as PropType<string>,
      required: true,
    },
    error: {
      type: String as PropType<string>,
    }
  },
  data() {
    return {
      selected: this.modelValue,
    }
  },
  watch: {
    selected(selected: string) {
      this.$emit('update:modelValue', selected)
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
