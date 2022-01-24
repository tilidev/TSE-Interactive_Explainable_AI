import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import DatasetExplorer from "../views/DatasetExplorer.vue";
import InstancePage from "../views/InstancePage.vue";
import ExperimentPage from "../views/ExperimentPage.vue"

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/dataset",
    name: "Dataset Explorer",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: DatasetExplorer,
  },
  {
    path: "/applications/:id",
    name: "Application View",
    component: InstancePage,
  },
  {
    path:"/experiments/:experimentId",
    name:"Experiment Page",
    component: ExperimentPage
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
