import { Inertia } from '@inertiajs/inertia'

declare module '@vue/runtime-core' {
  export interface ComponentCustomProperties {
    $route: (name: string, args?: Record<string, unknown> | string) => string
    $inertia: typeof Inertia
  }
}
