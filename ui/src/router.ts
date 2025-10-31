import { createRouter, createWebHashHistory } from 'vue-router'
import CardsView from './views/CardsView.vue'
import PendantsView from './views/PendantsView.vue'
import MapEventsView from './views/MapEventsView.vue'
import BeginEffectsView from './views/BeginEffectsView.vue'
import DSLHelp from './views/DSLHelp.vue'
import ShareView from './views/ShareView.vue'

const routes = [
  { path: '/', redirect: '/cards' },
  { path: '/cards', component: CardsView },
  { path: '/pendants', component: PendantsView },
  { path: '/map-events', component: MapEventsView },
  { path: '/begin-effects', component: BeginEffectsView },
  { path: '/help/effects', component: DSLHelp },
  { path: '/share', component: ShareView },
]

export default createRouter({
  history: createWebHashHistory(),
  routes
})
