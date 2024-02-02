const userRoutes = [
  {
    path: "", // 对应 "/user"
    redirect: "/user/login/"
  },
  {
    path: "login", // 对应 "/user/login"
    component: () => import("@/components/User/UserSignIn.vue"),
    props: { currentTabIndex: 1 }
  },
  {
    path: "signup", // 对应 "/user/signup"
    component: () => import("@/components/User/UserSignUp.vue"),
    props: { currentTabIndex: 2 }
  },
  {
    path: ":id(\\d+)?/:msg([^/]+)?", // 对应 "/user/:id/:msg"
    props: (route) => ({
      id: parseInt(route.params.id),
      msg: route.params.msg,
    })
  }
];

export default userRoutes;
