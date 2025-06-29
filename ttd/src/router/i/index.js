const EmptyComponent = {
  template: '<router-view></router-view>',
};

const toolRoutes = [
  {
    path: "", // 对应 "/i"
    name: "tool-root",
    meta: {isMeActive: false},
    component: EmptyComponent,
  },
  {
    path: "@me", // 对应 "/i"
    name: "tool-me",
    meta: {isMeActive: true}
  },
];

// Add dev-only routes in development mode
if (import.meta.env.DEV) {
  toolRoutes.push({
    path: "dev/icon-gallery",
    name: "dev-icon-gallery", 
    meta: {isMeActive: false},
    component: () => import("@/i/DevTools/IconGallery.vue")
  });
}

export default toolRoutes;
