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
import PlanningPage from '../views/PlanningPage.vue'
import MatchPage from '../views/MatchPage.vue'
import MatchCreatePage from '../views/MatchCreatePage.vue'
import MatchEditPage from '../views/MatchEditPage.vue'
import ChangePasswordPage from '../views/ChangePasswordPage.vue'

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
    path: '/user/create',
    name: 'user_create',
    component: UserCreatePage,
    meta: { requiresAuth: false }
  },
  {
    path: '/planning',
    name: 'planning',
    component: PlanningPage,
    meta: { requiresAuth: true }
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
  },
  {
    path: '/change-password',
    name: 'change_password',
    component: ChangePasswordPage,
    meta: { requiresAuth: true }
  }
  // TODO: Ajouter les autres routes (Planning, Résultats, Admin, Profil)
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard pour protéger les routes
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()

//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next('/login')
//   } else if (to.path === '/login' && authStore.isAuthenticated) {
//     next('/')
//   } else {
//     next()
//   }
// })

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Important: recharge token/user depuis localStorage si refresh
  authStore.checkAuth()

  const isLoggedIn = authStore.isAuthenticated
  const mustChange = authStore.user?.must_change_password === true

  // 1) Si route protégée et pas connecté => login
  if (to.meta.requiresAuth && !isLoggedIn) {
    return next('/login')
  }

  // 2) Si connecté, empêcher d'aller sur /login
  if (to.path === '/login' && isLoggedIn) {
    // si il doit changer mdp, on l'envoie là-bas
    return next(mustChange ? '/change-password' : '/')
  }

  // 3) Si connecté mais doit changer mdp => forcer /change-password
  if (isLoggedIn && mustChange && to.path !== '/change-password') {
    return next('/change-password')
  }

  // 4) (Optionnel) Si mdp déjà changé, empêcher de revenir sur /change-password
  if (isLoggedIn && !mustChange && to.path === '/change-password') {
    return next('/')
  }

  return next()
})


export default router
