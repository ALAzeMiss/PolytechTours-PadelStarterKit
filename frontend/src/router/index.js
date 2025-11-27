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
import PoulePage from '../views/PoulePage.vue'
import PouleCreatePage from '../views/PouleCreatePage.vue'
import PlayerPage from '../views/PlayerPage.vue'
import PlayerCreatePage from '../views/PlayerCreatePage.vue'

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
    meta: { requiresAuth: false }
  },
  {
    path: '/user/create',
    name: 'user_create',
    component: UserCreatePage,
    meta: { requiresAuth: false }
  },
  {
    path: '/equip',
    name: 'equip',
    component: EquipPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/equip/create',
    name: 'equip_create',
    component: EquipCreatePage,
    meta: { requiresAuth: false }
  },
  {
    path: '/poule',
    name: 'poule',
    component: PoulePage,
    meta: { requiresAuth: false }
  },
  {
    path: '/poule/create',
    name: 'poule_create',
    component: PouleCreatePage,
    meta: { requiresAuth: false }
  },
  {
    path: '/player',
    name: 'player',
    component: PlayerPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/player/create',
    name: 'player_create',
    component: PlayerCreatePage,
    meta: { requiresAuth: false }
  }
  // TODO: Ajouter les autres routes (Planning, Matchs, Résultats, Admin, Profil)
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
