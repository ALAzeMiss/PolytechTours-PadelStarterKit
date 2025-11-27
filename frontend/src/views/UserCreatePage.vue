<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Barre de nav -->
    <NavAdminBar/>
    
    <div class="max-w-4xl mx-auto p-20 text-center">
      <!-- Image ou logo -->
      <div class="mb-20">
        <div class="w-48 h-48 mx-auto bg-blue-600 rounded-full flex items-center justify-center text-white text-8xl shadow-2xl">
          🎾
        </div>
      </div>

      <!-- Message de Création -->
      <h1 class="text-5xl font-bold text-gray-800 mb-4">
        Création de User
      </h1>

      <!-- Contenu conditionnel -->
      <div v-if="authStore.isAuthenticated" class="space-y-4">

        <!-- Email -->
          <div class="mb-4">
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="votre@email.com"
            />
          </div>

        <label>
          <input type="checkbox" v-model="is_Admin" />
            Compte administrateur
        </label>

        <!--<p>Valeur : {{is_Admin}}</p> -->
      </div>

      <button
        type="submit"
        
        class="w-full py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        <span>Ajouter un profil</span>
      </button>

    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import NavAdminBar from '@/components/NavAdminBar.vue'

const authStore = useAuthStore()
</script>