<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <!-- Contenu principal centré -->
    <div class="flex flex-col items-center mt-10">

      <h1 class="text-3xl font-bold mb-8">
        Modifier l'équipe #{{ equipId }}
      </h1>

      <form class="bg-white shadow-lg rounded-xl p-8 w-full max-w-xl space-y-6" @submit.prevent="updateEquip">
        <div>
          <label class="font-semibold">Entreprise</label>
          <input v-model="form.entreprise" type="text" class="w-full p-2 rounded border" />
        </div>

        <div>
          <label class="font-semibold">Joueur 1</label>
          <input
            v-model="search1"
            type="text"
            class="w-full p-2 rounded border"
            placeholder="Rechercher un joueur"
            @focus="showDropdown1 = true"
            @blur="hideDropdown1"
          />
          <div v-if="showDropdown1 && filteredPlayers1.length" class="border rounded mt-1 max-h-40 overflow-y-auto bg-white">
            <div
              v-for="player in filteredPlayers1"
              :key="player.id"
              @mousedown="selectPlayer1(player)"
              class="p-2 hover:bg-gray-100 cursor-pointer"
            >
              {{ player.first_name }} {{ player.last_name }} (ID: {{ player.id }})
            </div>
          </div>
        </div>

        <div>
          <label class="font-semibold">Joueur 2</label>
          <input
            v-model="search2"
            type="text"
            class="w-full p-2 rounded border"
            placeholder="Rechercher un joueur"
            @focus="showDropdown2 = true"
            @blur="hideDropdown2"
          />
          <div v-if="showDropdown2 && filteredPlayers2.length" class="border rounded mt-1 max-h-40 overflow-y-auto bg-white">
            <div
              v-for="player in filteredPlayers2"
              :key="player.id"
              @mousedown="selectPlayer2(player)"
              class="p-2 hover:bg-gray-100 cursor-pointer"
            >
              {{ player.first_name }} {{ player.last_name }} (ID: {{ player.id }})
            </div>
          </div>
        </div>

        <div>
          <label class="font-semibold">Poule</label>
          <input v-model="form.poule" type="text" class="w-full p-2 rounded border bg-gray-100" disabled />
        </div>

        <button type="submit" class="w-full py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700">
          Enregistrer
        </button>
      </form>

    </div>

  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { ref, onMounted, computed } from 'vue'
import { playerAPI } from '../services/api'
import { useRoute, useRouter } from 'vue-router'
import { useTeamStore } from '../stores/team'

const route = useRoute()
const router = useRouter()
const equipId = route.params.id
const teamStore = useTeamStore()

const form = ref({
  entreprise: "",
  joueur1: "",
  joueur2: "",
  poule: ""
})

const players = ref([])
const search1 = ref('')
const search2 = ref('')
const showDropdown1 = ref(false)
const showDropdown2 = ref(false)

const filteredPlayers1 = computed(() => {
  if (!search1.value) return players.value
  return players.value.filter(player =>
    `${player.first_name} ${player.last_name} ${player.id}`.toLowerCase().includes(search1.value.toLowerCase())
  )
})

const filteredPlayers2 = computed(() => {
  if (!search2.value) return players.value
  return players.value.filter(player =>
    `${player.first_name} ${player.last_name} ${player.id}`.toLowerCase().includes(search2.value.toLowerCase())
  )
})

onMounted(async () => {
  try {
    const res = await teamStore.getTeam(equipId)
    form.value.entreprise = res.company
    form.value.joueur1 = res.player1_id.toString()
    form.value.joueur2 = res.player2_id.toString()
    form.value.poule = res.pool_id ? res.pool_id.toString() : ""
  } catch (err) {
    console.error(err)
    alert("Impossible de récupérer les informations de l'équipe")
  }

  try {
    const response = await playerAPI.getPlayers()
    players.value = response.data
    
    // Set search fields with current player names
    const player1 = players.value.find(p => p.id === parseInt(form.value.joueur1))
    const player2 = players.value.find(p => p.id === parseInt(form.value.joueur2))
    if (player1) {
      search1.value = `${player1.first_name} ${player1.last_name} (${player1.id})`
    }
    if (player2) {
      search2.value = `${player2.first_name} ${player2.last_name} (${player2.id})`
    }
  } catch (err) {
    console.error(err)
    alert("Impossible de récupérer les joueurs pour la sélection.")
  }
})

function selectPlayer1(player) {
  form.value.joueur1 = player.id.toString()
  search1.value = `${player.first_name} ${player.last_name} (${player.id})`
  showDropdown1.value = false
}

function selectPlayer2(player) {
  form.value.joueur2 = player.id.toString()
  search2.value = `${player.first_name} ${player.last_name} (${player.id})`
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

async function updateEquip() {
  if (!form.value.entreprise || !form.value.joueur1 || !form.value.joueur2) {
    alert("Veuillez remplir tous les champs.")
    return
  }
  
  // Validation de l'entreprise
  const companyRegex = /^[a-zA-ZÀ-ÿ0-9\s'-]{2,100}$/
  if (!companyRegex.test(form.value.entreprise)) {
    alert("L'entreprise doit contenir entre 2 et 100 caractères, uniquement des lettres, chiffres, espaces, apostrophes ou tirets.")
    return
  }
  
  // Validation des joueurs
  const joueur1Id = parseInt(form.value.joueur1)
  const joueur2Id = parseInt(form.value.joueur2)
  if (isNaN(joueur1Id) || isNaN(joueur2Id)) {
    alert("Les identifiants des joueurs doivent être des nombres.")
    return
  }
  if (joueur1Id === joueur2Id) {
    alert("Les deux joueurs doivent être différents.")
    return
  }
  
  // Vérifier que les joueurs existent
  const player1Exists = players.value.some(p => p.id === joueur1Id)
  const player2Exists = players.value.some(p => p.id === joueur2Id)
  if (!player1Exists) {
    alert("Le joueur 1 n'existe pas.")
    return
  }
  if (!player2Exists) {
    alert("Le joueur 2 n'existe pas.")
    return
  }
  
  // Préparer les données
  const data = {
    company: form.value.entreprise,
    player1_id: joueur1Id,
    player2_id: joueur2Id,
    pool_id: form.value.poule ? parseInt(form.value.poule) : null
  }
  
  try {
    await teamStore.updateTeam(equipId, data)
    alert("Modifications enregistrées")
    router.push('/equip')
  } catch (err) {
    console.error("Erreur détaillée:", err.response?.data || err.message)
    alert("Erreur lors de la mise à jour de l'équipe: " + (err.response?.data?.detail || err.message))
  }
}
</script>

<style scoped></style>
