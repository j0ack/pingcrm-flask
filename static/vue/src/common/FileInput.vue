<template>
  <div>
    <label v-if="label" class="form-label">{{ label }}:</label>
    <div class="form-input p-0" :class="{ error: errors.length }">
      <input ref="file" type="file" :accept="accept" class="hidden" @change="change" />
      <div v-if="!modelValue" class="p-2">
        <button
          type="button"
          class="px-4 py-1 bg-gray-500 hover:bg-gray-700 rounded-sm text-xs font-medium text-white"
          @click="browse"
        >
          Browse
        </button>
      </div>
      <div v-else class="flex items-center justify-between p-2">
        <div class="flex-1 pr-1">
          {{ modelValue.name }}
          <span class="text-gray-500 text-xs">({{ filesize(modelValue.size) }})</span>
        </div>
        <button
          type="button"
          class="px-4 py-1 bg-gray-500 hover:bg-gray-700 rounded-sm text-xs font-medium text-white"
          @click="remove"
        >
          Remove
        </button>
      </div>
    </div>
    <div v-if="errors.length" class="form-error">{{ errors[0] }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'


export default defineComponent({
  name: 'FileInput',
  props: {
    modelValue: {
      type: File as PropType<File>,
    },
    label: {
      type: String as PropType<string>,
      required: true
    },
    accept: {
      type: String as PropType<string>,
      required: true
    },
    errors: {
      type: Array as PropType<string[]>,
      default: () => [],
    },
  },
  watch: {
    modelValue(value) {
      if (!value) {
        (this.$refs.file as HTMLInputElement).value = ''
      }
    },
  },
  methods: {
    filesize(size: number) {
      const i: number = Math.floor(Math.log(size) / Math.log(1024))
      return (size / Math.pow(1024, i)).toFixed(2) + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i]
    },
    browse() {
      (this.$refs.file as HTMLInputElement).click()
    },
    change(e: InputEvent) {
      const files = (e.target as HTMLInputElement).files
      if (files) {
        this.$emit('input', files[0])
      }
    },
    remove() {
      this.$emit('input', null)
    },
  },
})
</script>
