<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <!-- Contenu principal -->
    <div class="flex justify-between items-center mb-4 p-6">
      <h1 class="text-2xl font-bold">Liste des poules</h1>

      <!-- Bouton Ajouter -->
      <button @click="handlePoule"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        🐔 Ajouter
      </button>
    </div>

    <div class="px-20">
      <table class="min-w-full bg-white border border-gray-300 rounded-lg shadow mx-2">
        <thead class="bg-light-100">
          <tr>
            <th class="py-2 px-4 border">Nom</th>
            <th class="py-2 px-4 border">Équipes</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="pool in poolStore.pools" :key="pool.id" class="hover:bg-gray-50">
            <td class="py-2 px-4 border">{{ pool.name }}</td>
            <td class="py-2 px-4 border">
              <div v-for="team in getTeamsForPool(pool.id)" :key="team.id" class="mb-1">
                {{ team.company }} ({{ team.player1_name }} / {{ team.player2_name }})
              </div>
            </td>

            <!-- Actions: Modifier / Supprimer -->
            <td class="py-2 px-4 border flex gap-6 justify-center">
              <!-- Crayon pour modifier -->
              <router-link :to="`/poule/edit/${pool.id}`">✏️</router-link>

              <!-- Poubelle pour supprimer -->
              <button @click="poolStore.deletePool(pool.id)" class="text-red-600 hover:text-red-800 text-xl">
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>


  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { useRouter } from 'vue-router'
import { onMounted, computed } from 'vue'
import { usePoolStore } from '../stores/pool'
import { useTeamStore } from '../stores/team'

const router = useRouter()
const poolStore = usePoolStore()
const teamStore = useTeamStore()

onMounted(async () => {
  await poolStore.getPools()
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
  } catch (err) {
    console.error('Erreur lors de la récupération des joueurs:', err)
  }
})

const getTeamsForPool = (poolId) => {
  return teamStore.teams.filter(team => team.pool_id === poolId)
}

const handlePoule = () => router.push('/poule/create')
</script>
