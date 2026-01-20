import { createRouter, createWebHistory } from 'vue-router'
import Login from './pages/Login.vue'
import Join from './pages/Join.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/join', component: Join }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router