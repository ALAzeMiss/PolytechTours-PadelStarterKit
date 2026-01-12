<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <!-- Contenu principal -->
    <div class="p-6 max-w-xl mx-auto">
      <h1 class="text-2xl font-bold mb-6">Création d'une poule</h1>
      <!-- Contenu principal -->
      <form class="space-y-4" @submit.prevent="handleValider">
        <div>
          <label class="block mb-1 font-medium">Nom de la poule</label>
          <input v-model="form.name" type="text" class="w-full p-2 rounded border" placeholder="Nom de la poule" />
        </div>

        <div>
          <label class="block mb-1 font-medium">Équipe 1</label>
          <input
            v-model="search1"
            type="text"
            class="w-full p-2 rounded border"
            placeholder="Rechercher une équipe"
            @focus="showDropdown1 = true"
            @blur="hideDropdown1"
          />
          <div v-if="showDropdown1 && filteredTeams1.length" class="border rounded mt-1 max-h-40 overflow-y-auto bg-white">
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

        <div>
          <label class="block mb-1 font-medium">Équipe 2</label>
          <input
            v-model="search2"
            type="text"
            class="w-full p-2 rounded border"
            placeholder="Rechercher une équipe"
            @focus="showDropdown2 = true"
            @blur="hideDropdown2"
          />
          <div v-if="showDropdown2 && filteredTeams2.length" class="border rounded mt-1 max-h-40 overflow-y-auto bg-white">
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

        <div>
          <label class="block mb-1 font-medium">Équipe 3</label>
          <input
            v-model="search3"
            type="text"
            class="w-full p-2 rounded border"
            placeholder="Rechercher une équipe"
            @focus="showDropdown3 = true"
            @blur="hideDropdown3"
          />
          <div v-if="showDropdown3 && filteredTeams3.length" class="border rounded mt-1 max-h-40 overflow-y-auto bg-white">
            <div
              v-for="team in filteredTeams3"
              :key="team.id"
              @mousedown="selectTeam3(team)"
              class="p-2 hover:bg-gray-100 cursor-pointer"
            >
              {{ team.company }} ({{ team.player1_name }} / {{ team.player2_name }})
            </div>
          </div>
        </div>

        <div>
          <label class="block mb-1 font-medium">Équipe 4</label>
          <input
            v-model="search4"
            type="text"
            class="w-full p-2 rounded border"
            placeholder="Rechercher une équipe"
            @focus="showDropdown4 = true"
            @blur="hideDropdown4"
          />
          <div v-if="showDropdown4 && filteredTeams4.length" class="border rounded mt-1 max-h-40 overflow-y-auto bg-white">
            <div
              v-for="team in filteredTeams4"
              :key="team.id"
              @mousedown="selectTeam4(team)"
              class="p-2 hover:bg-gray-100 cursor-pointer"
            >
              {{ team.company }} ({{ team.player1_name }} / {{ team.player2_name }})
            </div>
          </div>
        </div>

        <div>
          <label class="block mb-1 font-medium">Équipe 5</label>
          <input
            v-model="search5"
            type="text"
            class="w-full p-2 rounded border"
            placeholder="Rechercher une équipe"
            @focus="showDropdown5 = true"
            @blur="hideDropdown5"
          />
          <div v-if="showDropdown5 && filteredTeams5.length" class="border rounded mt-1 max-h-40 overflow-y-auto bg-white">
            <div
              v-for="team in filteredTeams5"
              :key="team.id"
              @mousedown="selectTeam5(team)"
              class="p-2 hover:bg-gray-100 cursor-pointer"
            >
              {{ team.company }} ({{ team.player1_name }} / {{ team.player2_name }})
            </div>
          </div>
        </div>

        <div>
          <label class="block mb-1 font-medium">Équipe 6</label>
          <input
            v-model="search6"
            type="text"
            class="w-full p-2 rounded border"
            placeholder="Rechercher une équipe"
            @focus="showDropdown6 = true"
            @blur="hideDropdown6"
          />
          <div v-if="showDropdown6 && filteredTeams6.length" class="border rounded mt-1 max-h-40 overflow-y-auto bg-white">
            <div
              v-for="team in filteredTeams6"
              :key="team.id"
              @mousedown="selectTeam6(team)"
              class="p-2 hover:bg-gray-100 cursor-pointer"
            >
              {{ team.company }} ({{ team.player1_name }} / {{ team.player2_name }})
            </div>
          </div>
        </div>

        <div class="flex justify-center">
          <button type="submit"
            class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition center">
            Valider
          </button>
        </div>
      </form>
    </div>


  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTeamStore } from '../stores/team'
import { usePoolStore } from '../stores/pool'
import { teamAPI } from '../services/api'

const router = useRouter()
const teamStore = useTeamStore()
const poolStore = usePoolStore()

const teams = ref([])
const search1 = ref('')
const search2 = ref('')
const search3 = ref('')
const search4 = ref('')
const search5 = ref('')
const search6 = ref('')
const showDropdown1 = ref(false)
const showDropdown2 = ref(false)
const showDropdown3 = ref(false)
const showDropdown4 = ref(false)
const showDropdown5 = ref(false)
const showDropdown6 = ref(false)

const form = ref({
  name: '',
  team_ids: []
})

const availableTeams = computed(() => {
  return teams.value.filter(team => team.pool_id === null && !form.value.team_ids.includes(team.id))
})

const filteredTeams1 = computed(() => {
  if (!search1.value) return availableTeams.value
  return availableTeams.value.filter(team =>
    `${team.company} ${team.player1_name} ${team.player2_name}`.toLowerCase().includes(search1.value.toLowerCase())
  )
})

const filteredTeams2 = computed(() => {
  if (!search2.value) return availableTeams.value
  return availableTeams.value.filter(team =>
    `${team.company} ${team.player1_name} ${team.player2_name}`.toLowerCase().includes(search2.value.toLowerCase())
  )
})

const filteredTeams3 = computed(() => {
  if (!search3.value) return availableTeams.value
  return availableTeams.value.filter(team =>
    `${team.company} ${team.player1_name} ${team.player2_name}`.toLowerCase().includes(search3.value.toLowerCase())
  )
})

const filteredTeams4 = computed(() => {
  if (!search4.value) return availableTeams.value
  return availableTeams.value.filter(team =>
    `${team.company} ${team.player1_name} ${team.player2_name}`.toLowerCase().includes(search4.value.toLowerCase())
  )
})

const filteredTeams5 = computed(() => {
  if (!search5.value) return availableTeams.value
  return availableTeams.value.filter(team =>
    `${team.company} ${team.player1_name} ${team.player2_name}`.toLowerCase().includes(search5.value.toLowerCase())
  )
})

const filteredTeams6 = computed(() => {
  if (!search6.value) return availableTeams.value
  return availableTeams.value.filter(team =>
    `${team.company} ${team.player1_name} ${team.player2_name}`.toLowerCase().includes(search6.value.toLowerCase())
  )
})

onMounted(async () => {
  await teamStore.getTeams()
  teams.value = teamStore.teams
  
  // Enrich with player names
  try {
    const playersResponse = await fetch('/api/v1/players/players')
    const players = await playersResponse.json()
    
    teams.value.forEach(team => {
      const player1 = players.find(p => p.id === team.player1_id)
      const player2 = players.find(p => p.id === team.player2_id)
      team.player1_name = player1 ? `${player1.first_name} ${player1.last_name}` : 'Inconnu'
      team.player2_name = player2 ? `${player2.first_name} ${player2.last_name}` : 'Inconnu'
    })
  } catch (err) {
    console.error('Erreur lors de la récupération des joueurs:', err)
  }
})

function selectTeam1(team) {
  form.value.team_ids[0] = team.id
  search1.value = `${team.company} (${team.player1_name} / ${team.player2_name})`
  showDropdown1.value = false
}

function selectTeam2(team) {
  form.value.team_ids[1] = team.id
  search2.value = `${team.company} (${team.player1_name} / ${team.player2_name})`
  showDropdown2.value = false
}

function selectTeam3(team) {
  form.value.team_ids[2] = team.id
  search3.value = `${team.company} (${team.player1_name} / ${team.player2_name})`
  showDropdown3.value = false
}

function selectTeam4(team) {
  form.value.team_ids[3] = team.id
  search4.value = `${team.company} (${team.player1_name} / ${team.player2_name})`
  showDropdown4.value = false
}

function selectTeam5(team) {
  form.value.team_ids[4] = team.id
  search5.value = `${team.company} (${team.player1_name} / ${team.player2_name})`
  showDropdown5.value = false
}

function selectTeam6(team) {
  form.value.team_ids[5] = team.id
  search6.value = `${team.company} (${team.player1_name} / ${team.player2_name})`
  showDropdown6.value = false
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

function hideDropdown3() {
  setTimeout(() => {
    showDropdown3.value = false
  }, 150)
}

function hideDropdown4() {
  setTimeout(() => {
    showDropdown4.value = false
  }, 150)
}

function hideDropdown5() {
  setTimeout(() => {
    showDropdown5.value = false
  }, 150)
}

function hideDropdown6() {
  setTimeout(() => {
    showDropdown6.value = false
  }, 150)
}

async function handleValider() {
  if (!form.value.name) {
    alert("Veuillez saisir le nom de la poule.")
    return
  }
  
  const selectedTeams = form.value.team_ids.filter(id => id)
  if (selectedTeams.length !== 6) {
    alert("Veuillez sélectionner 6 équipes.")
    return
  }
  
  const data = {
    name: form.value.name,
    team_ids: selectedTeams
  }
  
  try {
    await poolStore.createPool(data)
    alert("La poule a bien été créée !")
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
    alert("Erreur lors de la création de la poule: " + errorMsg)
  }
}
</script>
