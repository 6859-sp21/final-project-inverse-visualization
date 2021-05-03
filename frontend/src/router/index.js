import Vue from "vue";
import VueRouter from "vue-router";
import Editor from "../views/Editor.vue";
import Examples from "../views/Examples.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/editor",
    name: "Editor",
    component: Editor,
  },
  {
    path: "/",
    name: "Home",
    component: Examples,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
