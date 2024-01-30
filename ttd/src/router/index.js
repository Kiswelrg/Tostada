import { createRouter, createWebHistory } from "vue-router"
import User from '../user/User.vue'
import NotFound from '../components/NotFound.vue'
import Tool from '../i/App.vue'
import Empty from '../components/Util/Empty.vue'


const routes = [
  {
    path: "/user",
    component: User,
    children: [
      {
        path: "", // 对应 "/user"
        props: { currentTabIndex: 0 }
      },
      {
        path: "login", // 对应 "/user/login"
        component: Empty,
        props: { currentTabIndex: 1 }
      },
      {
        path: "signup", // 对应 "/user/signup"
        props: { currentTabIndex: 2 }
      },
      {
        path: ":id(\\d+)?/:msg([^/]+)?", // 对应 "/user/:id/:msg"
        props: (route) => ({
          id: parseInt(route.params.id),
          msg: route.params.msg,
        })
      }
    ]
  },
  {
    path: "/", // 根路径
    redirect: "/user" // 重定向到 "/user"
  },
  {
    path: "/i", // 工具路径
    component: Tool
  },
  {
    path: "/:unknownPath(.*)", // 未知路径
    component: NotFound
  }
];


// const routes = [
//   { path: "/", component: User, 
//   props: {currentTabIndex: 0}
//   },
//   { path: "/i/", component: Tool },
//   { path: "/user/login/", component: User, 
//     props: {currentTabIndex: 1}
//   },
//   { path: "/user/signup", component: User, 
//     props: {currentTabIndex: 2}
//   },
//   {
//     path: "/user/:id(\\d+)?/:msg([^/]+)?/",
//     component: User,
//     props: (route) => ({
//       id: parseInt(route.params.id),
//       msg: route.params.msg,
//     }),
//   },
//   { path: "/:unknownPath(.*)", component: NotFound },
// ];

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

