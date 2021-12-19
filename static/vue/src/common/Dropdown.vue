<template>
  <button type="button" @click="show = true">
    <slot />
    <Teleport v-if="show" to="#dropdown">
      <div>
        <div id="modal" @click="show = false" />
        <div ref="dropdown" style="position: absolute; z-index: 99999;" @click.stop="show = autoClose ? false : true">
          <slot name="dropdown" />
        </div>
      </div>
    </Teleport>
  </button>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import { createPopper, Instance, Placement } from '@popperjs/core';

export default defineComponent({
  name: 'Dropdown',
  props: {
    placement: {
      type: String as PropType<Placement>,
      default: 'bottom-end',
    },
    boundary: {
      type: String as PropType<string>,
      default: 'scrollParent',
    },
    autoClose: {
      type: Boolean as PropType<boolean>,
      default: true,
    },
  },
  data() {
    return {
      show: false,
      popper: null as Instance | null
    }
  },
  watch: {
    show(show) {
      if (show) {
        this.$nextTick(() => {
          const dropdown = this.$refs.dropdown as HTMLElement
          this.popper = createPopper(this.$el, dropdown, {
            placement: this.placement,
            modifiers: [
              {
                name: 'preventOverflow',
                options: { boundariesElement: this.boundary },
              }
            ],
          })
        })
      } else if (this.popper) {
        setTimeout(() => {
          if (this.popper) { this.popper.destroy() }
        }, 100)
      }
    },
  },
  mounted() {
    document.addEventListener('keydown', e => {
      if (e.keyCode === 27) {
        this.show = false
      }
    })
  },
})
</script>

<style scoped>
#modal {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  z-index: 99998;
  background: black;
  opacity: .2;
}
</style>
