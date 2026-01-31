<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <div class="max-w-2xl mx-auto p-6">
      <div class="bg-white rounded-lg shadow-lg p-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">Créer un match</h1>

        <!-- Message d'erreur -->
        <div v-if="error" class="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
          {{ error }}
        </div>

        <form @submit.prevent="handleSubmit">
          <!-- Date -->
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
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Heure -->
          <div class="mb-4">
            <label for="match_time" class="block text-sm font-medium text-gray-700 mb-2">
              Heure du match *
            </label>
            <input
              type="time"
              id="match_time"
              v-model="formData.match_time"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
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

          <!-- Équipe 1 -->
          <div class="mb-4">
            <label for="team1_search" class="block text-sm font-medium text-gray-700 mb-2">
              Équipe 1 *
            </label>
            <input
              id="team1_search"
              v-model="search1"
              type="text"
              placeholder="Rechercher une équipe"
              @focus="showDropdown1 = true"
              @blur="hideDropdown1"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div v-if="showDropdown1 && filteredTeams1.length" class="border border-gray-300 rounded-lg mt-1 max-h-40 overflow-y-auto bg-white">
              <div
                v-for="team in filteredTeams1"
                :key="team.id"
                @mousedown="selectTeam1(team)"
                class="p-2 hover:bg-gray-100 cursor-pointer"
              >
                {{ team.company }} ({{ team.player1_name }} / {{ team.player2_name }})
              </div>
            </div>
          </div>

          <!-- Équipe 2 -->
          <div class="mb-4">
            <label for="team2_search" class="block text-sm font-medium text-gray-700 mb-2">
              Équipe 2 *
            </label>
            <input
              id="team2_search"
              v-model="search2"
              type="text"
              placeholder="Rechercher une équipe"
              @focus="showDropdown2 = true"
              @blur="hideDropdown2"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div v-if="showDropdown2 && filteredTeams2.length" class="border border-gray-300 rounded-lg mt-1 max-h-40 overflow-y-auto bg-white">
              <div
                v-for="team in filteredTeams2"
                :key="team.id"
                @mousedown="selectTeam2(team)"
                class="p-2 hover:bg-gray-100 cursor-pointer"
              >
                {{ team.company }} ({{ team.player1_name }} / {{ team.player2_name }})
              </div>
            </div>
          </div>

          <!-- Boutons -->
          <div class="flex gap-4 mt-6">
            <button
              type="submit"
              :disabled="loading"
              class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {{ loading ? 'Création...' : 'Créer le match' }}
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
import { useRouter } from 'vue-router'
import { matchAPI, teamAPI, playerAPI } from '@/services/api'

const router = useRouter()

const formData = ref({
  match_date: '',
  match_time: '',
  court_number: 1,
  team1_id: '',
  team2_id: '',
  status: 'A_VENIR'
})

const teams = ref([])
const search1 = ref('')
const search2 = ref('')
const showDropdown1 = ref(false)
const showDropdown2 = ref(false)
const loading = ref(false)
const error = ref('')

const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

const filteredTeams1 = computed(() => {
  if (!search1.value) return teams.value
  return teams.value.filter(team =>
    `${team.company} ${team.player1_name} ${team.player2_name}`.toLowerCase().includes(search1.value.toLowerCase())
  )
})

const filteredTeams2 = computed(() => {
  if (!search2.value) return teams.value
  return teams.value.filter(team =>
    `${team.company} ${team.player1_name} ${team.player2_name}`.toLowerCase().includes(search2.value.toLowerCase())
  )
})

const fetchTeamsAndPlayers = async () => {
  try {
    const teamsResponse = await teamAPI.getTeams()
    const playersResponse = await playerAPI.getPlayers()
    
    const players = playersResponse.data
    
    // Enrichir les équipes avec les noms des joueurs
    teams.value = teamsResponse.data.map(team => ({
      ...team,
      player1_name: players.find(p => p.id === team.player1_id)
        ? `${players.find(p => p.id === team.player1_id).first_name} ${players.find(p => p.id === team.player1_id).last_name}`
        : 'Inconnu',
      player2_name: players.find(p => p.id === team.player2_id)
        ? `${players.find(p => p.id === team.player2_id).first_name} ${players.find(p => p.id === team.player2_id).last_name}`
        : 'Inconnu'
    }))
  } catch (err) {
    error.value = 'Erreur lors du chargement des équipes'
    console.error('Erreur:', err)
  }
}

function selectTeam1(team) {
  formData.value.team1_id = team.id
  search1.value = `${team.company} (${team.player1_name} / ${team.player2_name})`
  showDropdown1.value = false
}

function selectTeam2(team) {
  formData.value.team2_id = team.id
  search2.value = `${team.company} (${team.player1_name} / ${team.player2_name})`
  showDropdown2.value = false
}

function hideDropdown1() {
  setTimeout(() => {
    showDropdown1.value = false
  }, 150)
}

function hideDropdown2() {
  setTimeout(() => {
    showDropdown2.value = false
  }, 150)
}

const handleSubmit = async () => {
  error.value = ''
  
  // Validation
  if (formData.value.team1_id === formData.value.team2_id) {
    error.value = 'Les deux équipes doivent être différentes'
    return
  }
  
  loading.value = true
  
  try {
    await matchAPI.createMatch(formData.value)
    // Ajouter un délai pour s'assurer que le serveur a créé le match
    await new Promise(resolve => setTimeout(resolve, 500))
    router.push('/matches')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la création du match'
    console.error('Erreur:', err)
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  router.push('/matches')
}

onMounted(() => {
  fetchTeamsAndPlayers()
})
</script>
