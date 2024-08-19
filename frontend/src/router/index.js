import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import HistoryView from '@/views/HistoryView.vue'
import DeatilsVue from '@/views/DeatilsVue.vue'
import comingsoon from '@/views/comingsoon.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryView
    },
    {
      path: '/details/:id',
      name: 'details',
      component: DeatilsVue
    },
    {
      path: '/comingsoon',
      name: 'comingsoon',
      component: comingsoon
    }
  ]
})

export default router
