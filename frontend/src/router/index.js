import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UploadView from '../views/UploadView.vue'
import DataView from '../views/DataView.vue'
import VisualizationView from '../views/VisualizationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/upload',
      name: 'upload',
      component: UploadView
    },
    {
      path: '/data',
      name: 'data',
      component: DataView
    },
    {
      path: '/visualization',
      name: 'visualization',
      component: VisualizationView
    }
  ]
})

export default router 