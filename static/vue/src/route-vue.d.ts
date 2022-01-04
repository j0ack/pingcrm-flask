import { Inertia } from '@inertiajs/inertia'

type StrOrNum = string | number

declare module '@vue/runtime-core' {
  export interface ComponentCustomProperties {
    $route: (urlName: string, args?: Record<string, unknown> | StrOrNum | StrOrNum[]): string
    $inertia: typeof Inertia
  }
}
