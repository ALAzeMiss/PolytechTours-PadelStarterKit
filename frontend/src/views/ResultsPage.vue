<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Barre de nav -->
    <NavBar v-if="authStore.user?.role === 'JOUEUR'" />
    <NavAdminBar v-else />

    <div class="p-6">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">Résultats</h1>

      <!-- Message d'erreur -->
      <div v-if="error" class="mb-4 p-4 bg-red-100 text-red-700 rounded-lg text-center">
        {{ error }}
      </div>

      <!-- Section Résultats personnels (Joueurs uniquement) -->
      <div v-if="authStore.user?.role === 'JOUEUR'" class="mb-8">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-semibold text-gray-800">Mes Résultats</h2>
          
          <!-- Filtre par saison -->
          <div class="flex items-center gap-2">
            <label for="seasonFilter" class="text-sm font-medium text-gray-700">Période :</label>
            <select 
              id="seasonFilter"
              v-model="seasonFilter"
              @change="fetchPersonalResults"
              class="px-3 py-2 border rounded-lg"
            >
              <option value="current">Depuis le début de la saison</option>
              <option value="">Tous les résultats</option>
            </select>
          </div>
        </div>

        <!-- Message de chargement -->
        <div v-if="loadingPersonal" class="text-center py-12 bg-white rounded-lg shadow">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p class="text-lg text-gray-600">Chargement de vos résultats...</p>
        </div>

        <!-- Liste des résultats -->
        <div v-else class="bg-white rounded-lg shadow overflow-hidden">
          <table class="min-w-full">
            <thead class="bg-gray-100">
              <tr>
                <th class="py-3 px-4 text-left border">Date</th>
                <th class="py-3 px-4 text-left border">Adversaires</th>
                <th class="py-3 px-4 text-left border">Score</th>
                <th class="py-3 px-4 text-left border">Piste</th>
              </tr>
            </thead>

            <tbody>
              <tr v-if="personalResults.length === 0">
                <td colspan="4" class="py-12 px-4 text-center">
                  <div class="flex flex-col items-center justify-center">
                    <div class="text-6xl mb-4">🎾</div>
                    <p class="text-xl font-semibold text-gray-700 mb-2">Aucun résultat trouvé</p>
                    <p class="text-sm text-gray-500">Vous n'avez pas encore de matchs terminés</p>
                  </div>
                </td>
              </tr>
              <tr v-for="result in personalResults" :key="result.id" class="hover:bg-gray-50 border-b">
                <!-- Date -->
                <td class="py-3 px-4">
                  <div class="font-medium">{{ formatDateDDMMYYYY(result.match_date) }}</div>
                </td>

                <!-- Adversaires -->
                <td class="py-3 px-4">
                  <div class="font-medium">{{ result.adversary_company }}</div>
                  <div class="text-sm text-gray-600">{{ result.adversary_player1_name }}</div>
                  <div class="text-sm text-gray-600">{{ result.adversary_player2_name }}</div>
                </td>

                <!-- Score avec couleur -->
                <td class="py-3 px-4">
                  <span 
                    :class="{
                      'text-green-600 font-bold': result.is_victory,
                      'text-red-600 font-bold': !result.is_victory
                    }"
                  >
                    {{ formatScore(result) }}
                  </span>
                </td>

                <!-- Piste -->
                <td class="py-3 px-4">
                  <span class="inline-block px-3 py-1 bg-gray-200 rounded-full text-sm font-medium">
                    {{ result.court_number }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Classement général des entreprises -->
      <div class="mt-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Classement Général</h2>

        <!-- Message de chargement -->
        <div v-if="loadingRanking" class="text-center py-12 bg-white rounded-lg shadow">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p class="text-lg text-gray-600">Chargement du classement...</p>
        </div>

        <!-- Tableau de classement -->
        <div v-else class="bg-white rounded-lg shadow overflow-hidden">
          <table class="min-w-full">
            <thead class="bg-gray-100">
              <tr>
                <th class="py-3 px-4 text-center border">Position</th>
                <th class="py-3 px-4 text-left border">Entreprise</th>
                <th class="py-3 px-4 text-center border">Matchs joués</th>
                <th class="py-3 px-4 text-center border">Victoires</th>
                <th class="py-3 px-4 text-center border">Défaites</th>
                <th class="py-3 px-4 text-center border">Points</th>
              </tr>
            </thead>

            <tbody>
              <tr v-if="ranking.length === 0">
                <td colspan="6" class="py-12 px-4 text-center">
                  <div class="flex flex-col items-center justify-center">
                    <div class="text-6xl mb-4">🏆</div>
                    <p class="text-xl font-semibold text-gray-700 mb-2">Aucun classement disponible</p>
                    <p class="text-sm text-gray-500">Il n'y a pas encore de résultats</p>
                  </div>
                </td>
              </tr>
              <tr 
                v-for="item in ranking" 
                :key="item.company" 
                class="hover:bg-gray-50 border-b"
                :class="{ 'bg-yellow-50': item.position === 1, 'bg-gray-50': item.position === 2 || item.position === 3 }"
              >
                <!-- Position -->
                <td class="py-3 px-4 text-center">
                  <span class="text-lg font-bold">
                    {{ item.position === 1 ? '🥇' : item.position === 2 ? '🥈' : item.position === 3 ? '🥉' : item.position }}
                  </span>
                </td>

                <!-- Entreprise -->
                <td class="py-3 px-4">
                  <div class="font-medium text-lg">{{ item.company }}</div>
                </td>

                <!-- Matchs joués -->
                <td class="py-3 px-4 text-center">
                  {{ item.matches_played }}
                </td>

                <!-- Victoires -->
                <td class="py-3 px-4 text-center">
                  <span class="text-green-600 font-semibold">{{ item.victories }}</span>
                </td>

                <!-- Défaites -->
                <td class="py-3 px-4 text-center">
                  <span class="text-red-600 font-semibold">{{ item.defeats }}</span>
                </td>

                <!-- Points -->
                <td class="py-3 px-4 text-center">
                  <span class="text-blue-600 font-bold text-lg">{{ item.points }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { resultsAPI } from '@/services/api'
import NavBar from '@/components/NavBar.vue'
import NavAdminBar from '@/components/NavAdminBar.vue'

const authStore = useAuthStore()

const personalResults = ref([])
const ranking = ref([])
const loadingPersonal = ref(false)
const loadingRanking = ref(false)
const error = ref('')
const seasonFilter = ref('current')

const formatDateDDMMYYYY = (dateStr) => {
  const date = new Date(dateStr)
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()
  return `${day}/${month}/${year}`
}

const formatScore = (result) => {
  // Déterminer le score à afficher en fonction de l'équipe du joueur
  if (result.user_team_id === result.id) {
    return result.score_team1 || 'N/A'
  }
  
  // Afficher le score dans l'ordre logique (joueur vs adversaire)
  // Si l'utilisateur était team1, afficher score_team1 - score_team2
  // Sinon afficher score_team2 - score_team1
  const userScore = result.score_team1
  const advScore = result.score_team2
  
  if (!userScore || !advScore) return 'N/A'
  
  return `${userScore} vs ${advScore}`
}

const fetchPersonalResults = async () => {
  if (authStore.user?.role !== 'JOUEUR') return
  
  loadingPersonal.value = true
  error.value = ''
  
  try {
    const params = {}
    if (seasonFilter.value) {
      params.season_filter = seasonFilter.value
    }
    
    const response = await resultsAPI.getPersonalResults(params)
    personalResults.value = response.data
  } catch (err) {
    let errorMsg = 'Erreur lors du chargement de vos résultats'
    
    if (err.response?.data?.detail) {
      errorMsg = err.response.data.detail
    }
    
    error.value = errorMsg
    console.error('Erreur:', err)
  } finally {
    loadingPersonal.value = false
  }
}

const fetchRanking = async () => {
  loadingRanking.value = true
  error.value = ''
  
  try {
    const response = await resultsAPI.getCompanyRanking()
    ranking.value = response.data
  } catch (err) {
    let errorMsg = 'Erreur lors du chargement du classement'
    
    if (err.response?.data?.detail) {
      errorMsg = err.response.data.detail
    }
    
    error.value = errorMsg
    console.error('Erreur:', err)
  } finally {
    loadingRanking.value = false
  }
}

onMounted(() => {
  if (authStore.user?.role === 'JOUEUR') {
    fetchPersonalResults()
  }
  fetchRanking()
})
</script>
