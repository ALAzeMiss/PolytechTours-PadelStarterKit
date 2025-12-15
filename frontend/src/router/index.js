// ============================================
// FICHIER : frontend/src/router/index.js
// ============================================

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import HomePage from '../views/HomePage.vue'
import LoginPage from '../views/LoginPage.vue'
import AdminPage from '../views/AdminPage.vue'
import ProfilePage from '../views/ProfilePage.vue'
import UserCreatePage from '../views/UserCreatePage.vue'
import EquipPage from '../views/EquipPage.vue'
import EquipCreatePage from '../views/EquipCreatePage.vue'
import EquipEditPage from '../views/EquipEditPage.vue'
import PoulePage from '../views/PoulePage.vue'
import PouleCreatePage from '../views/PouleCreatePage.vue'
import PouleEditPage from '../views/PouleEditPage.vue'
import PlayerPage from '../views/PlayerPage.vue'
import PlayerCreatePage from '../views/PlayerCreatePage.vue'
import PlayerEditPage from '../views/PlayerEditPage.vue'
import MatchPage from '../views/MatchPage.vue'
import MatchCreatePage from '../views/MatchCreatePage.vue'
import MatchEditPage from '../views/MatchEditPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'user_create',
    component: UserCreatePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/equip',
    name: 'equip',
    component: EquipPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/equip/create',
    name: 'equip_create',
    component: EquipCreatePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/equip/edit/:id',
    name: 'edit-equip',
    component: EquipEditPage,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/poule',
    name: 'poule',
    component: PoulePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/poule/create',
    name: 'poule_create',
    component: PouleCreatePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/poule/edit/:id',
    name: 'edit-poule',
    component: PouleEditPage,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/players',
    name: 'players',
    component: PlayerPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/players/create',
    name: 'players_create',
    component: PlayerCreatePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/players/edit/:id',
    name: 'edit-player',
    component: PlayerEditPage,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/matches',
    name: 'matches',
    component: MatchPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/matches/create',
    name: 'match_create',
    component: MatchCreatePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/matches/edit/:id',
    name: 'edit-match',
    component: MatchEditPage,
    meta: { requiresAuth: true },
    props: true
  }
  // TODO: Ajouter les autres routes (Planning, Résultats, Admin, Profil)
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard pour protéger les routes
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
