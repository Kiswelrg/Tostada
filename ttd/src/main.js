import { createApp } from 'vue'
import '@/style.css'
import App from './App.vue'
import router from './router'
import { library, icon } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faSmile,
  faPen,
  faEllipsisH,
  faArrowLeft,
  faTrash,
  faClipboard,
  faPaperclip,
  faDownload,
  faMicrophone,
  faHeadphones,
  faHashtag,
  faGear,
} from "@fortawesome/free-solid-svg-icons";
import clickOutside from './util/directives/clickOutside'


library.add(
    faSmile,
    faPen,
    faEllipsisH,
    faArrowLeft,
    faTrash, faClipboard, faPaperclip,
    faDownload,
    faMicrophone,
    faHeadphones,
    faHashtag,
    faGear,
)

const app = createApp(App)
            .component('font-awesome-icon', FontAwesomeIcon)
            .use(router)
app.directive('click-outside', clickOutside)
app.mount('#app')
