import { createApp } from 'vue'
import '@/style.css'
import App from './App.vue'
import router from './router'
import { library, icon } from '@fortawesome/fontawesome-svg-core'
import { faSmile, faPen, faEllipsisH, faArrowLeft } from '@fortawesome/free-solid-svg-icons'
import clickOutside from './util/directives/clickOutside'


library.add(
    faSmile,
    faPen,
    faEllipsisH,
    faArrowLeft,
)

const app = createApp(App).use(router)
app.directive('click-outside', clickOutside)
app.mount('#app')
