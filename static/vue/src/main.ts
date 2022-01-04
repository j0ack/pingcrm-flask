import { createApp, h, App } from 'vue'
import { createInertiaApp } from '@inertiajs/inertia-vue3'
import '@/css/app.css'

type StrOrNum = string | number

declare global {
  interface Window {
    reverseUrl(urlName: string, args?: Record<string, unknown> | StrOrNum | StrOrNum[]): string
  }
}

const routeConfig = {
  install: (app: App, _options: Record<string, unknown>) => {
    app.config.globalProperties.$route = window.reverseUrl
  }
}

createInertiaApp({
  resolve: async name => {
    const page = await import(`./pages/${name}`)
    return page.default
  },
  setup({ el, app, props, plugin }) {
    const vueApp = createApp({ render: () => h(app, props) })
    vueApp.use(plugin)
    vueApp.use(routeConfig)
    vueApp.mount(el)
  }
})
