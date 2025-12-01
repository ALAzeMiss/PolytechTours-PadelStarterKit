// ============================================
// FICHIER : frontend/src/stores/user.js
// ============================================

import { defineStore } from 'pinia'
import { userAPI } from '@/services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    selectedUser: null,      // utilisateur affiché ou édité
    users: [],               // liste des utilisateurs (si nécessaire)
    loading: false,
    error: null
  }),

  actions: {

    // Charger un utilisateur selon son ID
    async fetchUser(userId) {
      this.loading = true
      this.error = null
      try {
        const res = await userAPI.getUser(userId)
        this.selectedUser = res.data
      } catch (err) {
        this.error = err.response?.data || 'Erreur lors du chargement'
      } finally {
        this.loading = false
      }
    },

    // Créer un utilisateur
    async createUser(userData) {
      this.loading = true
      this.error = null
      try {
        const res = await userAPI.createUser(userData)
        return res.data
      } catch (err) {
        this.error = err.response?.data || 'Erreur lors de la création'
        throw err
      } finally {
        this.loading = false
      }
    },

    // Mettre à jour un utilisateur
    async updateUser(userId, userData) {
      this.loading = true
      this.error = null
      try {
        const res = await userAPI.updateUser(userId, userData)
        this.selectedUser = res.data
        return res.data
      } catch (err) {
        this.error = err.response?.data || 'Erreur lors de la mise à jour'
        throw err
      } finally {
        this.loading = false
      }
    },

    // Supprimer un utilisateur
    async deleteUser(userId) {
      this.loading = true
      this.error = null
      try {
        await userAPI.deleteUser(userId)
        this.selectedUser = null
      } catch (err) {
        this.error = err.response?.data || 'Erreur lors de la suppression'
        throw err
      } finally {
        this.loading = false
      }
    },

    // Regénérer un mot de passe
    async regeneratePassword() {
      this.loading = true
      this.error = null
      try {
        const res = await userAPI.regeneratePassword()
        return res.data
      } catch (err) {
        this.error = err.response?.data || 'Erreur lors de la génération'
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})
