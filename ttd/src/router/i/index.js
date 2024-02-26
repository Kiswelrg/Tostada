const toolRoutes = [
  {
    path: "", // 对应 "/i"
    name: "tool-root",
    meta: {isMeActive: false}
  },
  {
    path: "@me", // 对应 "/i"
    name: "tool-me",
    meta: {isMeActive: true}
  },
];

export default toolRoutes;
