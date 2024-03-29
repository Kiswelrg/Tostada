import { createRouter, createWebHashHistory, createWebHistory } from "vue-router"
import User from '../account/User.vue'
import NotFound from '../components/NotFound.vue'
import Tool from '../i/App.vue'
import Empty from '../components/Util/Empty.vue'
import userRoutes from "./user"
import toolRoutes from "./i"
import user_util from "@/util/user"

const routes = [
  {
    path: "/", // 根路径
    name: "root",
    component: () => import("@/main/MainTemp.vue"),
  },
  {
    path: "/a",
    name: "account",
    component: User,
    children: userRoutes
  },
  {
    path: "/i", // 工具路径
    name: "tool",
    component: Tool,
    children: toolRoutes
  },
  {
    path: "/:unknownPath(.*)", // 未知路径
    name: "404",
    component: NotFound
  }
];


// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
  // 4. Provide the history implementation to use. We are using the ×hash× history for simplicity here.
  history: createWebHistory(),
  routes, // short for `routes: routes`
  sensitive: true,
  // strict: true,
});

router.beforeEach(async (to, from, next) => {
  const isLoggedIn = await user_util.checkLoggedIn()
  if (to.matched[0].name == 'tool') {
    if (isLoggedIn['r'] == 0)
      next({ name : 'user-login' })
    else {
      next()
    }
  } else next()
})

export default router;

