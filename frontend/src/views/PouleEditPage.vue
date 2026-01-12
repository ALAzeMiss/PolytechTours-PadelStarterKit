<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <!-- Contenu principal centré -->
    <div class="flex flex-col items-center mt-10">

      <h1 class="text-3xl font-bold mb-8">
        Modifier la poule #{{ poolId }}
      </h1>

      <form class="bg-white shadow-lg rounded-xl p-8 w-full max-w-xl space-y-6" @submit.prevent="updatePool">
        <div>
          <label class="block mb-1 font-medium">Nom de la poule</label>
          <input v-model="form.name" type="text" class="w-full p-2 rounded border" placeholder="Nom de la poule" />
        </div>

        <div v-for="(team, index) in currentTeams" :key="team.id" class="border p-2 rounded">
          <label class="font-semibold">Équipe {{ index + 1 }} (lecture seule)</label>
          <input
            :value="`${team.company} (${team.player1_name} / ${team.player2_name})`"
            type="text"
            class="w-full p-2 rounded border bg-gray-100"
            disabled
          />
        </div>

        <button type="submit"
          class="w-full py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700">
          Enregistrer
        </button>
      </form>

    </div>

  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePoolStore } from '../stores/pool'
import { useTeamStore } from '../stores/team'

const route = useRoute()
const router = useRouter()
const poolId = route.params.id
const poolStore = usePoolStore()
const teamStore = useTeamStore()

const form = ref({
  name: ''
})

const currentTeams = ref([])

onMounted(async () => {
  try {
    const pool = await poolStore.getPool(poolId)
    form.value.name = pool.name
  } catch (err) {
    console.error('Erreur lors du chargement de la poule:', err)
    alert("Impossible de récupérer les informations de la poule")
  }

  await teamStore.getTeams()
  
  // Enrich teams with player names
  try {
    const playersResponse = await fetch('/api/v1/players/players')
    const players = await playersResponse.json()
    
    teamStore.teams.forEach(team => {
      const player1 = players.find(p => p.id === team.player1_id)
      const player2 = players.find(p => p.id === team.player2_id)
      team.player1_name = player1 ? `${player1.first_name} ${player1.last_name}` : 'Inconnu'
      team.player2_name = player2 ? `${player2.first_name} ${player2.last_name}` : 'Inconnu'
    })
    
    // Get teams for this pool
    currentTeams.value = teamStore.teams.filter(team => team.pool_id === parseInt(poolId))
  } catch (err) {
    console.error('Erreur lors de la récupération des équipes:', err)
  }
})

async function updatePool() {
  if (!form.value.name) {
    alert("Veuillez saisir le nom de la poule.")
    return
  }
  
  try {
    await poolStore.updatePool(poolId, { name: form.value.name })
    alert("Modifications enregistrées")
    router.push('/poule')
  } catch (err) {
    console.error("Erreur détaillée:", err.response?.data || err.message)
    let errorMsg = err.message
    if (err.response?.data?.detail) {
      if (Array.isArray(err.response.data.detail)) {
        errorMsg = err.response.data.detail.map(d => d.msg || d).join(', ')
      } else {
        errorMsg = err.response.data.detail
      }
    }
    alert("Erreur lors de la mise à jour de la poule: " + errorMsg)
  }
}
</script>

<style scoped>
</style>
