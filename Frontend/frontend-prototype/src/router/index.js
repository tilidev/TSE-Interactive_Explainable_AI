import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Level1 from '../views/Level1.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/level1',
    name: 'Level1',
    component: Level1
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
