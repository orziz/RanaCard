import { createRouter, createWebHashHistory } from 'vue-router'
import CardsView from './views/CardsView.vue'
import PendantsView from './views/PendantsView.vue'

const routes = [
  { path: '/', redirect: '/cards' },
  { path: '/cards', component: CardsView },
  { path: '/pendants', component: PendantsView }
]

export default createRouter({
  history: createWebHashHistory(),
  routes
})

