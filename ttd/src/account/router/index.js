import { createRouter, createWebHistory } from "vue-router"
import User from "../User.vue"
import Home from '../Home/Home.vue'
import Signup from "../Signup/Signup.vue"

// import NotFound from "../components/NotFound.vue";


const routes = [
  {
    path: "/account/:num(\\d+)?/",
    component: User,
    props: (route) => ({
      num: parseInt(route.params.num),
    }),
  },
  {
    path: "/account/:id(\\d+)?/:msg([^/]+)?/",
    component: User,
    props: (route) => ({
      id: parseInt(route.params.id),
      msg: route.params.msg,
    }),
  },
  // { path: "/:unknownPath(.*)", component: NotFound },
]

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
  // 4. Provide the history implementation to use. We are using the ×hash× history for simplicity here.
  history: createWebHistory('/account/'),
  routes, // short for `routes: routes`
  sensitive: true,
})

export default router
