import { createRouter, createWebHistory } from "vue-router";
import Parts from "./components/Parts.vue";
import Clients from "./components/Clients.vue";
import Services from "./components/Services.vue";
import Visits from "./components/Visits.vue";
import NotFound from "./components/NotFound.vue";
import Home from "./components/Home.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/parts",
      name: "Parts",
      component: Parts,
    },
    {
      path: "/clients",
      name: "Clients",
      component: Clients,
    },
    {
      path: "/services",
      name: "Services",
      component: Services,
    },
    {
      path: "/visits",
      name: "Visits",
      component: Visits,
    },
    {
      path: "/:pathMatch(.*)*",
      name: "NotFound",
      component: NotFound,
    },
    {
      path: "/",
      name: "Home",
      component: Home,
    },
  ],
});
