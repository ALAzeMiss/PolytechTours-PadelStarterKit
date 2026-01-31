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
            <h3 class="font-medium text-gray-700 mb-3">Scores (sets)</h3>

            <p class="text-xs text-gray-500 mb-3">
              Format attendu : <strong>X-Y, X-Y</strong> ou <strong>X-Y, X-Y, X-Y</strong><br />
              Exemple : <strong>6-4, 3-6, 7-5</strong><br />
              L’équipe 2 doit être l’inverse : <strong>4-6, 6-3, 5-7</strong>
            </p>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="score_team1" class="block text-sm font-medium text-gray-700 mb-2">
                  Score Équipe 1 *
                </label>
                <input
                  type="text"
                  id="score_team1"
                  v-model.trim="formData.score_team1"
                  placeholder='Ex: 7-5, 6-4'
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label for="score_team2" class="block text-sm font-medium text-gray-700 mb-2">
                  Score Équipe 2 *
                </label>
                <input
                  type="text"
                  id="score_team2"
                  v-model.trim="formData.score_team2"
                  placeholder='Ex: 5-7, 4-6'
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <p v-if="scoreError" class="mt-3 text-sm text-red-600 font-medium">
              {{ scoreError }}
            </p>
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
import { ref, onMounted, computed, watch } from 'vue'
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
  score_team1: '',
  score_team2: '',
})

const currentMatch = ref(null)
const loadingMatch = ref(false)
const loading = ref(false)
const error = ref('')
const scoreError = ref('')

const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// ---------- Validation front (basique + inverse exact) ----------
const parseSets = (scoreStr) => {
  if (!scoreStr) return []
  return scoreStr
    .split(',')
    .map(s => s.trim())
    .filter(Boolean)
    .map(setStr => {
      const m = setStr.match(/^(\d+)\s*-\s*(\d+)$/)
      if (!m) return null
      return [Number(m[1]), Number(m[2])]
    })
}

const validateInverseScores = () => {
  scoreError.value = ''

  if (formData.value.status !== 'TERMINE') return true

  const s1raw = formData.value.score_team1?.trim()
  const s2raw = formData.value.score_team2?.trim()

  if (!s1raw || !s2raw) {
    scoreError.value = 'Les deux scores sont obligatoires lorsque le match est terminé.'
    return false
  }

  const s1 = parseSets(s1raw)
  const s2 = parseSets(s2raw)

  if (s1.length < 2 || s1.length > 3 || s2.length < 2 || s2.length > 3) {
    scoreError.value = 'Un match doit contenir 2 ou 3 sets (ex: "6-4, 3-6, 7-5").'
    return false
  }

  if (s1.includes(null) || s2.includes(null)) {
    scoreError.value = 'Format invalide. Utilisez "X-Y, X-Y" (ex: "6-4, 7-5").'
    return false
  }

  if (s1.length !== s2.length) {
    scoreError.value = 'Les deux scores doivent contenir le même nombre de sets.'
    return false
  }

  for (let i = 0; i < s1.length; i++) {
    const [a1, b1] = s1[i]
    const [a2, b2] = s2[i]
    if (a2 !== b1 || b2 !== a1) {
      scoreError.value = `Incohérence au set ${i + 1} : Équipe 2 doit avoir ${b1}-${a1}.`
      return false
    }
  }

  return true
}

// Revalider en live
watch(
  () => [formData.value.status, formData.value.score_team1, formData.value.score_team2],
  () => { validateInverseScores() }
)


const fetchMatch = async () => {
  loadingMatch.value = true
  error.value = ''
  scoreError.value = ''
  
  try {
    const response = await matchAPI.getMatch(matchId)
    currentMatch.value = response.data
    
    // Remplir le formulaire
    formData.value = {
      match_date: response.data.match_date,
      match_time: response.data.match_time.substring(0, 5), // Format HH:MM
      court_number: response.data.court_number,
      status: response.data.status,
      score_team1: response.data.score_team1 ?? '',
      score_team2: response.data.score_team2 ?? ''
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
  scoreError.value = ''

  if (!validateInverseScores()) return
  
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
