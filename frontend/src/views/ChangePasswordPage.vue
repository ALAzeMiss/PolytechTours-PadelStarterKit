<!-- ============================================
FICHIER : frontend/src/views/ChangePasswordPage.vue
============================================ -->

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="w-full max-w-md">
      <div class="bg-white rounded-lg shadow-2xl p-8">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="text-6xl mb-4">🔒</div>
          <h1 class="text-3xl font-bold text-gray-800">Changer le mot de passe</h1>
          <p class="text-gray-600 mt-2">
            Pour continuer, vous devez définir un nouveau mot de passe.
          </p>
        </div>

        <!-- Formulaire -->
        <form @submit.prevent="handleChangePassword">
          <!-- Ancien mot de passe -->
          <div class="mb-4">
            <label for="currentPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Mot de passe actuel
            </label>
            <div class="relative">
              <input
                id="currentPassword"
                v-model="currentPassword"
                :type="showCurrent ? 'text' : 'password'"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-12"
                placeholder="••••••••"
                autocomplete="current-password"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 px-3 text-gray-500 hover:text-gray-700"
                @click="showCurrent = !showCurrent"
                aria-label="Afficher/masquer le mot de passe actuel"
              >
                {{ showCurrent ? '🙈' : '👁️' }}
              </button>
            </div>
          </div>

          <!-- Nouveau mot de passe -->
          <div class="mb-4">
            <label for="newPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Nouveau mot de passe
            </label>
            <div class="relative">
              <input
                id="newPassword"
                v-model="newPassword"
                :type="showNew ? 'text' : 'password'"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-12"
                placeholder="••••••••"
                autocomplete="new-password"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 px-3 text-gray-500 hover:text-gray-700"
                @click="showNew = !showNew"
                aria-label="Afficher/masquer le nouveau mot de passe"
              >
                {{ showNew ? '🙈' : '👁️' }}
              </button>
            </div>

            <!-- Hint règles -->
            <p class="text-xs text-gray-500 mt-2">
              Conseil : utilisez au moins 8 caractères, avec une majuscule, une minuscule, un chiffre et un symbole.
            </p>
          </div>

          <!-- Confirmation -->
          <div class="mb-6">
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Confirmer le nouveau mot de passe
            </label>
            <div class="relative">
              <input
                id="confirmPassword"
                v-model="confirmPassword"
                :type="showConfirm ? 'text' : 'password'"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-12"
                placeholder="••••••••"
                autocomplete="new-password"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 px-3 text-gray-500 hover:text-gray-700"
                @click="showConfirm = !showConfirm"
                aria-label="Afficher/masquer la confirmation"
              >
                {{ showConfirm ? '🙈' : '👁️' }}
              </button>
            </div>
          </div>

          <!-- Erreurs -->
          <div v-if="errorMessage" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-700 text-sm">{{ errorMessage }}</p>
          </div>

          <!-- Succès -->
          <div v-if="successMessage" class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p class="text-green-700 text-sm">{{ successMessage }}</p>
          </div>

          <!-- Bouton -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Enregistrement...</span>
            <span v-else>Mettre à jour</span>
          </button>
        </form>

        <!-- Déconnexion (optionnel mais pratique) -->
        <button
          type="button"
          class="w-full mt-4 py-3 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
          @click="handleLogout"
          :disabled="loading"
        >
          Se déconnecter
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authAPI } from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const showCurrent = ref(false)
const showNew = ref(false)
const showConfirm = ref(false)

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

function validate() {
  errorMessage.value = ''
  successMessage.value = ''

  if (newPassword.value.length < 8) {
    errorMessage.value = 'Le nouveau mot de passe doit contenir au moins 8 caractères.'
    return false
  }

  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = 'La confirmation ne correspond pas au nouveau mot de passe.'
    return false
  }

  if (newPassword.value === currentPassword.value) {
    errorMessage.value = 'Le nouveau mot de passe doit être différent de l’ancien.'
    return false
  }

  return true
}

const handleChangePassword = async () => {
  if (!validate()) return

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await authAPI.changePassword(
      currentPassword.value,
      newPassword.value,
      confirmPassword.value
    )

    // Mettre à jour le store : l'utilisateur n'est plus forcé de changer son mdp
    if (authStore.user) {
      authStore.user.must_change_password = false
      localStorage.setItem('user', JSON.stringify(authStore.user))
    }

    successMessage.value = 'Mot de passe modifié avec succès.'
    // Redirection
    router.push('/')
  } catch (err) {
    const data = err.response?.data

    // Ton backend renvoie parfois detail string, parfois detail object
    const detail = data?.detail

    if (typeof detail === 'string') {
      errorMessage.value = detail
    } else if (typeof detail === 'object' && detail?.message) {
      errorMessage.value = detail.message
    } else {
      errorMessage.value = 'Erreur lors du changement de mot de passe.'
    }
  } finally {
    loading.value = false
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>
