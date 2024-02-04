import { createRouter, createWebHashHistory, createWebHistory } from "vue-router"
import User from '../user/User.vue'
import NotFound from '../components/NotFound.vue'
import Tool from '../i/App.vue'
import Empty from '../components/Util/Empty.vue'
import userRoutes from "./user"
import toolRoutes from "./i"


const routes = [
  {
    path: "/", // 根路径
    component: () => import("@/main/MainTemp.vue"),
  },
  {
    path: "/user",
    component: User,
    children: userRoutes
  },
  {
    path: "/i", // 工具路径
    component: Tool,
    children: toolRoutes
  },
  {
    path: "/:unknownPath(.*)", // 未知路径
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
  strict: true,
});



export default router;

