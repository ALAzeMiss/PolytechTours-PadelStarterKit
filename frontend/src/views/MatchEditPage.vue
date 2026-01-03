<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
  

    <div class="max-w-2xl mx-auto p-6">
      <div class="bg-white rounded-lg shadow-lg p-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">Modifier le match</h1>

        <!-- Message d'erreur -->
        <div v-if="error" class="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
          {{ error }}
        </div>

        <!-- Message de chargement -->
        <div v-if="loadingMatch" class="text-center py-8">
          <p class="text-gray-600">Chargement du match...</p>
        </div>

        <form v-else @submit.prevent="handleSubmit">
          <!-- Date (modifiable uniquement si statut = A_VENIR) -->
          <div class="mb-4">
            <label for="match_date" class="block text-sm font-medium text-gray-700 mb-2">
              Date du match *
            </label>
            <input
              type="date"
              id="match_date"
              v-model="formData.match_date"
              required
              :min="minDate"
              :disabled="currentMatch?.status !== 'A_VENIR'"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            />
            <p v-if="currentMatch?.status !== 'A_VENIR'" class="text-xs text-gray-500 mt-1">
              La date ne peut être modifiée que pour les matchs à venir
            </p>
          </div>

          <!-- Heure (modifiable uniquement si statut = A_VENIR) -->
          <div class="mb-4">
            <label for="match_time" class="block text-sm font-medium text-gray-700 mb-2">
              Heure du match *
            </label>
            <input
              type="time"
              id="match_time"
              v-model="formData.match_time"
              required
              :disabled="currentMatch?.status !== 'A_VENIR'"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            />
            <p v-if="currentMatch?.status !== 'A_VENIR'" class="text-xs text-gray-500 mt-1">
              L'heure ne peut être modifiée que pour les matchs à venir
            </p>
          </div>

          <!-- Piste -->
          <div class="mb-4">
            <label for="court_number" class="block text-sm font-medium text-gray-700 mb-2">
              Numéro de piste * (1-10)
            </label>
            <input
              type="number"
              id="court_number"
              v-model.number="formData.court_number"
              required
              min="1"
              max="10"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Statut -->
          <div class="mb-4">
            <label for="status" class="block text-sm font-medium text-gray-700 mb-2">
              Statut *
            </label>
            <select
              id="status"
              v-model="formData.status"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="A_VENIR">À venir</option>
              <option value="ANNULE">Annulé</option>
              <option value="TERMINE">Terminé</option>
            </select>
          </div>

          <!-- Scores (si match terminé) -->
          <div v-if="formData.status === 'TERMINE'" class="mb-4 p-4 bg-gray-50 rounded-lg">
            <h3 class="font-medium text-gray-700 mb-3">Scores</h3>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="score_team1" class="block text-sm font-medium text-gray-700 mb-2">
                  Score Équipe 1
                </label>
                <input
                  type="number"
                  id="score_team1"
                  v-model.number="formData.score_team1"
                  min="0"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label for="score_team2" class="block text-sm font-medium text-gray-700 mb-2">
                  Score Équipe 2
                </label>
                <input
                  type="number"
                  id="score_team2"
                  v-model.number="formData.score_team2"
                  min="0"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          <!-- Informationséquipes (lecture seule) -->
          <div class="mb-4 p-4 bg-blue-50 rounded-lg">
            <h3 class="font-medium text-gray-700 mb-2">Équipes</h3>
            <div v-if="currentMatch" class="text-sm text-gray-600">
              <p><strong>Équipe 1:</strong> {{ currentMatch.team1.company }}</p>
              <p><strong>Équipe 2:</strong> {{ currentMatch.team2.company }}</p>
            </div>
          </div>

          <!-- Boutons -->
          <div class="flex gap-4 mt-6">
            <button
              type="submit"
              :disabled="loading"
              class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {{ loading ? 'Enregistrement...' : 'Enregistrer' }}
            </button>
            <button
              type="button"
              @click="handleCancel"
              class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { matchAPI } from '@/services/api'

const router = useRouter()
const route = useRoute()

const matchId = route.params.id

const formData = ref({
  match_date: '',
  match_time: '',
  court_number: 1,
  status: 'A_VENIR',
  score_team1: null,
  score_team2: null
})

const currentMatch = ref(null)
const loadingMatch = ref(false)
const loading = ref(false)
const error = ref('')

const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

const fetchMatch = async () => {
  loadingMatch.value = true
  error.value = ''
  
  try {
    const response = await matchAPI.getMatch(matchId)
    currentMatch.value = response.data
    
    // Remplir le formulaire
    formData.value = {
      match_date: response.data.match_date,
      match_time: response.data.match_time.substring(0, 5), // Format HH:MM
      court_number: response.data.court_number,
      status: response.data.status,
      score_team1: response.data.score_team1,
      score_team2: response.data.score_team2
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors du chargement du match'
    console.error('Erreur:', err)
  } finally {
    loadingMatch.value = false
  }
}

const handleSubmit = async () => {
  error.value = ''
  loading.value = true
  
  try {
    await matchAPI.updateMatch(matchId, formData.value)
    router.push('/matches')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la modification du match'
    console.error('Erreur:', err)
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  router.push('/matches')
}

onMounted(() => {
  fetchMatch()
})
</script>
