import { createRouter, createWebHistory } from "vue-router";
import Home from "../components/Home.vue";
import SignUp from "../components/SignUp.vue";
import User from "../components/User.vue";
import NotFound from "../components/NotFound.vue";


const routes = [
  { path: "/", component: Home },
  { path: "/signup", component: SignUp },
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
