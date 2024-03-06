import { createApp } from 'vue'
import '@/style.css'
import App from './App.vue'
import router from './router'
import { library, icon } from '@fortawesome/fontawesome-svg-core'
import { faSmile, faPen, faEllipsisH } from '@fortawesome/free-solid-svg-icons'

library.add(
    faSmile,
    faPen,
    faEllipsisH
)

createApp(App)
    .use(router)
    .mount('#app')
