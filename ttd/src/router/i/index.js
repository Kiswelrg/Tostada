const toolRoutes = [
  {
    path: "", // 对应 "/i"
    name: "tool-root",
    component: () => import("@/i/FunctionDetail/Server/Server.vue"),
  },
  {
    path: "@me", // 对应 "/i"
    name: "tool-me",
    component: () => import("@/i/FunctionDetail/me/me.vue"),
  },
];

export default toolRoutes;
