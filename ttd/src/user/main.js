import { createApp } from 'vue'
import '@/style.css'
import App from './User.vue'
import router from './router'


// app.use(router)
createApp(App)
    .use(router)
    .mount('#app')
