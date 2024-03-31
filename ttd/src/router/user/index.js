const userRoutes = [
  {
    path: "", // 对应 "/user"
    name: "user-root",
    redirect: "/account/login/"
  },
  {
    path: "logout/", // 对应 "/user"
    redirect: "/account/login/"
  },
  {
    path: "login/", // 对应 "/account/login"
    alias: 'signin/',
    name: "user-login",
    component: () => import("@/components/Account/UserSignIn.vue"),
    props: { currentTabIndex: 1 }
  },
  {
    path: "signup/", // 对应 "/account/signup"
    component: () => import("@/components/Account/UserSignUp.vue"),
    props: { currentTabIndex: 2 }
  },
  {
    path: "forgetpassword/", // 对应 "/account/signup"
    component: () => import("@/components/Account/UserForgetPassword.vue"),
    props: { currentTabIndex: 2 }
  },
  {
    path: ":id(\\d+)?/:msg([^/]+)?/", // 对应 "/account/:id/:msg"
    props: (route) => ({
      id: parseInt(route.params.id),
      msg: route.params.msg,
    })
  }
];

export default userRoutes;
