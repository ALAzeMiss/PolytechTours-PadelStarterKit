<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <div class="flex justify-between items-center mb-4 p-6">
      <h1 class="text-2xl font-bold">Liste des équipes</h1>

      <!-- Bouton Ajouter -->
      <button @click="handleEquip"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        ➕ Ajouter
      </button>
    </div>

    <div class="px-20">
      <table class="min-w-full bg-white border border-blue-300 rounded-lg shadow mx-2">
        <thead class="bg-light-100">
          <tr>
            <th class="py-2 px-4 border">Entreprise</th>
            <th class="py-2 px-4 border">Joueur 1</th>
            <th class="py-2 px-4 border">Joueur 2</th>
            <th class="py-2 px-4 border">Poule</th>
            <th class="py-2 px-4 border">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="team in teamStore.teams" :key="team.id" class="hover:bg-gray-50">
            <td class="py-2 px-4 border">{{ team.company }}</td>
            <td class="py-2 px-4 border">{{ team.player1_name }}</td>
            <td class="py-2 px-4 border">{{ team.player2_name }}</td>
            <td class="py-2 px-4 border">{{ team.pool_id }}</td>

            <!-- Actions: Modifier / Supprimer -->
            <td class="py-2 px-4 border flex gap-6 justify-center">
              <!-- Crayon pour modifier -->
              <router-link :to="`/equip/edit/${team.id}`">✏️</router-link>

              <!-- Poubelle pour supprimer -->
              <button @click="teamStore.deleteTeam(team.id)" class="text-red-600 hover:text-red-800 text-xl">
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
import { onMounted } from 'vue'
import { useTeamStore } from '../stores/team'
import { playerAPI } from '../services/api'

const router = useRouter()
const teamStore = useTeamStore()

onMounted(async () => {
  await teamStore.getTeams()
  
  try {
    const playersResponse = await playerAPI.getPlayers()
    const players = playersResponse.data
    
    // Enrich teams with player names
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


const handleEquip = () => router.push('/equip/create')
</script>

<style scoped></style>