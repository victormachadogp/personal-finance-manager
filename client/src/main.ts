import './assets/main.css'
import PrimeVue from 'primevue/config'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import { createServiceProvider } from './plugins/serviceProvider'
import router from './router'

const isDemoMode = import.meta.env.VITE_DEMO_MODE === 'true'
const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue)

app.use(createServiceProvider(isDemoMode))

app.mount('#app')
