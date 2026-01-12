<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Barre de nav -->
    <NavBar v-if="authStore.user?.is_admin === false" />


    <div class="p-6">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-3xl font-bold text-gray-800">Matchs à venir</h1>
        
        <!-- Bouton Ajouter (admin uniquement) -->
        <button 
          v-if="authStore.user?.is_admin === true"
          @click="handleCreate"
          class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          ➕ Ajouter un match
        </button>
      </div>

      <!-- Filtres -->
      <div class="mb-6 p-4 bg-white rounded-lg shadow">
        <!-- Filtre pour les joueurs -->
        <div v-if="authStore.user?.is_admin === false" class="flex items-center gap-2">
          <input 
            type="checkbox" 
            id="showAll" 
            v-model="showAll"
            @change="fetchMatches"
            class="w-4 h-4"
          />
          <label for="showAll" class="text-sm font-medium text-gray-700">
            Voir tous les matchs
          </label>
        </div>

        <!-- Filtres pour les admins -->
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Entreprise</label>
            <input 
              type="text" 
              v-model="filters.company"
              @input="fetchMatches"
              placeholder="Filtrer par entreprise"
              class="w-full px-3 py-2 border rounded-lg"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Poule</label>
            <input 
              type="number" 
              v-model="filters.pool_id"
              @input="fetchMatches"
              placeholder="ID de la poule"
              class="w-full px-3 py-2 border rounded-lg"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Statut</label>
            <select 
              v-model="filters.status"
              @change="fetchMatches"
              class="w-full px-3 py-2 border rounded-lg"
            >
              <option value="">Tous</option>
              <option value="A_VENIR">À venir</option>
              <option value="ANNULE">Annulé</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Message d'erreur -->
      <div v-if="error" class="mb-4 p-4 bg-red-100 text-red-700 rounded-lg text-center">
        {{ error }}
      </div>

      <!-- Message de chargement -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
        <p class="text-lg text-gray-600">Chargement des matchs en cours...</p>
      </div>

      <!-- Tableau des matchs -->
      <div v-else class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full">
          <thead class="bg-gray-100">
            <tr>
              <th class="py-3 px-4 text-left border">Date et heure</th>
              <th class="py-3 px-4 text-left border">Piste</th>
              <th class="py-3 px-4 text-left border">Équipes</th>
              <th class="py-3 px-4 text-left border">Joueurs</th>
              <th class="py-3 px-4 text-left border">Statut</th>
              <th v-if="authStore.user?.is_admin === true" class="py-3 px-4 text-center border">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="matches.length === 0">
              <td :colspan="authStore.user?.is_admin === true ? 6 : 5" class="py-12 px-4 text-center">
                <div class="flex flex-col items-center justify-center">
                  <div class="text-6xl mb-4">🎾</div>
                  <p class="text-xl font-semibold text-gray-700 mb-2">Aucun match trouvé</p>
                  <p class="text-sm text-gray-500">
                    {{ authStore.user?.is_admin === false && !showAll 
                      ? 'Cochez "Voir tous les matchs" pour voir tous les matchs disponibles' 
                      : 'Il n\'y a aucun match prévu dans les 30 prochains jours' }}
                  </p>
                </div>
              </td>
            </tr>
            <tr v-for="match in matches" :key="match.id" class="hover:bg-gray-50 border-b">
              <!-- Date et heure -->
              <td class="py-3 px-4">
                <div class="font-medium">{{ formatDate(match.match_date) }}</div>
                <div class="text-sm text-gray-600">à {{ formatTime(match.match_time) }}</div>
              </td>

              <!-- Piste -->
              <td class="py-3 px-4">
                <span class="inline-block px-3 py-1 bg-gray-200 rounded-full text-sm font-medium">
                  Piste {{ match.court_number }}
                </span>
              </td>

              <!-- Équipes -->
              <td class="py-3 px-4">
                <div class="font-medium">{{ match.team1.company }}</div>
                <div class="text-sm text-gray-500">vs</div>
                <div class="font-medium">{{ match.team2.company }}</div>
              </td>

              <!-- Joueurs -->
              <td class="py-3 px-4">
                <div class="text-sm">
                  <div>{{ match.team1.player1.first_name }} {{ match.team1.player1.last_name }}</div>
                  <div>{{ match.team1.player2.first_name }} {{ match.team1.player2.last_name }}</div>
                  <div class="text-gray-400 my-1">—</div>
                  <div>{{ match.team2.player1.first_name }} {{ match.team2.player1.last_name }}</div>
                  <div>{{ match.team2.player2.first_name }} {{ match.team2.player2.last_name }}</div>
                </div>
              </td>

              <!-- Statut -->
              <td class="py-3 px-4">
                <span 
                  :class="{
                    'bg-blue-100 text-blue-800': match.status === 'A_VENIR',
                    'bg-red-100 text-red-800': match.status === 'ANNULE'
                  }"
                  class="inline-block px-3 py-1 rounded-full text-sm font-medium"
                >
                  {{ match.status === 'A_VENIR' ? 'À venir' : 'Annulé' }}
                </span>
              </td>

              <!-- Actions (admin uniquement) -->
              <td v-if="authStore.user?.is_admin === true" class="py-3 px-4">
                <div class="flex gap-2 justify-center">
                  <button 
                    @click="handleEdit(match.id)" 
                    class="text-blue-600 hover:text-blue-800 text-xl"
                    title="Modifier"
                  >
                    ✏️
                  </button>
                  <button 
                    @click="handleDelete(match.id)" 
                    class="text-red-600 hover:text-red-800 text-xl"
                    :disabled="match.status !== 'A_VENIR'"
                    :class="{ 'opacity-50 cursor-not-allowed': match.status !== 'A_VENIR' }"
                    title="Supprimer"
                  >
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { matchAPI } from '@/services/api'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const authStore = useAuthStore()

const matches = ref([])
const loading = ref(false)
const error = ref('')
const showAll = ref(false)
const filters = ref({
  company: '',
  pool_id: null,
  status: ''
})

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
  return date.toLocaleDateString('fr-FR', options)
}

const formatTime = (timeStr) => {
  // timeStr est au format HH:MM:SS ou HH:MM
  return timeStr.substring(0, 5)
}

const fetchMatches = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const params = {}
    
    // Filtres pour joueurs
    if (authStore.user?.is_admin === false) {
      params.show_all = showAll.value
    }
    
    // Filtres pour admins
    if (authStore.user?.is_admin === true) {
      if (filters.value.company) params.company = filters.value.company
      if (filters.value.pool_id) params.pool_id = filters.value.pool_id
      if (filters.value.status) params.status = filters.value.status
    }
    
    const response = await matchAPI.getMatches(params)
    matches.value = response.data
  } catch (err) {
    // Traduire les messages d'erreur en français
    let errorMsg = 'Erreur lors du chargement des matchs'
    
    if (err.response?.data?.detail) {
      errorMsg = err.response.data.detail
      // Traduire les messages anglais courants
      if (errorMsg === 'Not Found') errorMsg = 'Ressource introuvable'
      if (errorMsg === 'Unauthorized') errorMsg = 'Non autorisé'
      if (errorMsg === 'Forbidden') errorMsg = 'Accès refusé'
    }
    
    error.value = errorMsg
    console.error('Erreur:', err)
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  router.push('/matches/create')
}

const handleEdit = (matchId) => {
  router.push(`/matches/edit/${matchId}`)
}

const handleDelete = async (matchId) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer ce match ?')) {
    return
  }
  
  try {
    await matchAPI.deleteMatch(matchId)
    await fetchMatches()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la suppression du match'
    console.error('Erreur:', err)
  }
}

onMounted(() => {
  fetchMatches()
})
</script>
