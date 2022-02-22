import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import DatasetExplorer from "../views/DatasetExplorer.vue";
import InstancePage from "../views/InstancePage.vue";
import ExperimentPage from "../views/ExperimentPage.vue"
import TreeMapTestView from "../views/TreeMapTestView.vue"
import TreeMapTestView2 from "../views/TreeMapTestView2.vue"
import TreeMapTestView3 from "../views/TreeMapTestView3.vue"
import TreeMapTestView4 from "../views/TreeMapTestView4.vue"

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
  },
  {
    path: "/treemap",
    name: "TreeMapTestView",
    component: TreeMapTestView,
  },
  {
    path: "/treemap2",
    name: "TreeMapTestView2",
    component: TreeMapTestView2,
  },
  {
    path: "/treemap3",
    name: "TreeMapTestView3",
    component: TreeMapTestView3,
  },
  {
    path: "/treemap4",
    name: "TreeMapTestView4",
    component: TreeMapTestView4,
  }

];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
