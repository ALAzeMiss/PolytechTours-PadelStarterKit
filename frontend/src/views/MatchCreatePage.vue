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
            <label for="team1_id" class="block text-sm font-medium text-gray-700 mb-2">
              Équipe 1 *
            </label>
            <select
              id="team1_id"
              v-model.number="formData.team1_id"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Sélectionnez une équipe</option>
              <option v-for="team in teams" :key="team.id" :value="team.id">
                {{ team.company }} - {{ team.player1.first_name }} {{ team.player1.last_name }} & {{ team.player2.first_name }} {{ team.player2.last_name }}
              </option>
            </select>
          </div>

          <!-- Équipe 2 -->
          <div class="mb-4">
            <label for="team2_id" class="block text-sm font-medium text-gray-700 mb-2">
              Équipe 2 *
            </label>
            <select
              id="team2_id"
              v-model.number="formData.team2_id"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Sélectionnez une équipe</option>
              <option v-for="team in teams" :key="team.id" :value="team.id" :disabled="team.id === formData.team1_id">
                {{ team.company }} - {{ team.player1.first_name }} {{ team.player1.last_name }} & {{ team.player2.first_name }} {{ team.player2.last_name }}
              </option>
            </select>
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
import { matchAPI } from '@/services/api'
import api from '@/services/api'

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
const loading = ref(false)
const error = ref('')

const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

const fetchTeams = async () => {
  try {
    const response = await api.get('/teams')
    teams.value = response.data
  } catch (err) {
    error.value = 'Erreur lors du chargement des équipes'
    console.error('Erreur:', err)
  }
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
  fetchTeams()
})
</script>
