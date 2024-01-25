import { createApp } from 'vue'
import '@/style.css'
import App from './App.vue'
import router from './router'
import $ from 'jquery'

createApp(App)
    .use(router)
    .mount('#app')
