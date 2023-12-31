import { createRouter, createWebHistory } from "vue-router"
import User from '../user/User.vue'
import NotFound from '../components/NotFound.vue'
import Tool from '../i/App.vue'

const routes = [
  { path: "/", component: User, 
  props: {currentTabIndex: 0}
  },
  { path: "/i/", component: Tool },
  { path: "/user/login/", component: User, 
    props: {currentTabIndex: 1}
  },
  { path: "/user/signup", component: User, 
    props: {currentTabIndex: 2}
  },
  {
    path: "/user/:id(\\d+)?/:msg([^/]+)?/",
    component: User,
    props: (route) => ({
      id: parseInt(route.params.id),
      msg: route.params.msg,
    }),
  },
  { path: "/:unknownPath(.*)", component: NotFound },
];

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
  // 4. Provide the history implementation to use. We are using the ×hash× history for simplicity here.
  history: createWebHistory(),
  routes, // short for `routes: routes`
  sensitive: true,
});

export default router;
