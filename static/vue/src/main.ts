import { createApp, h } from 'vue'
import { createInertiaApp } from '@inertiajs/inertia-vue3'
import '@/css/app.css'

const container = document.getElementById('app')
if (!container) {
  throw 'Main container not found'
}

const pageData = (container.dataset || {}).page
if (!pageData) {
  throw 'No dataset page found in root container'
}

const routeConfig = {
  install: (app: any, options: any) => {
    app.config.globalProperties.$route = (window as any).reverseUrl
  }
}

createInertiaApp({
  resolve: async name => {
    const page = await import(`./pages/${name}`)
    return page.default
  },
  setup({ el, app, props, plugin }) {
    createApp({ render: () => h(app, props) })
      .use(plugin)
      .use(routeConfig)
      .mount(container)
  }
})
