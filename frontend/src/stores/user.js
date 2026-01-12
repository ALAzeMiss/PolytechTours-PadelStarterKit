// ============================================
// FICHIER : frontend/src/stores/user.js
// ============================================

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userAPI } from '@/services/api'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const users = ref([])

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin === true)

  // Créer un utilisateur
  async function createUser(userData) {
    loading.value = true
    error.value = null
    try {
      const res = await userAPI.createUser(userData)
      if (res?.data?.user) {
        users.value.unshift(res.data.user)
      }
      return res
    } catch (err) {
      error.value = err.response?.data || 'Erreur lors de la création'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function getUsers() {
    loading.value = true
    error.value = null
    try {
      const res = await userAPI.getUsers()
      users.value = res.data
      console.log(res)
      return res
    } catch (err) {
      error.value = err.response?.data || 'Erreur lors de la récupération'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Supprimer un utilisateur
  async function deleteUser(userId) {
    loading.value = true
    error.value = null
    try {
      await userAPI.deleteUser(userId)
    } catch (err) {
      error.value = err.response?.data || "Erreur lors de la suppression"
      throw err
    } finally {
      loading.value = false
    }
  }

  // Regénérer un mot de passe
  async function regeneratePassword() {
    loading.value = true
    error.value = null
    try {
      const res = await userAPI.regeneratePassword()
      return res.data
    } catch (err) {
      error.value = err.response?.data || "Erreur lors de la génération"
      throw err
    } finally {
      loading.value = false
    }
  }
  return {
    user,
    token,
    loading,
    error,
    users,
    isAuthenticated,
    isAdmin,
    createUser,
    getUsers,
    deleteUser,
    regeneratePassword
  }
})
