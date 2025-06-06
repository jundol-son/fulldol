import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import ApexCharts from 'vue3-apexcharts'

const app = createApp(App)
app.use(ApexCharts)
app.use(router)
app.mount('#app')
