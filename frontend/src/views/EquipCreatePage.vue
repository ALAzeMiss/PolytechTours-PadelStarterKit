<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />
    <div class="p-6 max-w-xl mx-auto">
      <h1 class="text-2xl font-bold mb-6">Création d'une équipe</h1>
      <!-- Contenu principal -->
      <form class="space-y-4">
        <div>
          <label class="block mb-1 font-medium">Entreprise</label>
          <input v-model="form.entreprise" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'entreprise" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Joueur 1</label>
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
          <label class="block mb-1 font-medium">Joueur 2</label>
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

        <div class="flex justify-center">
          <button @click="handleValider"
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
import { useRouter } from 'vue-router'
import { ref, onMounted, computed } from 'vue'
import { useTeamStore } from '../stores/team'
import { playerAPI } from '../services/api'

const teamStore = useTeamStore()
const router = useRouter()

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

const form = ref({
  entreprise: '',
  joueur1: '',
  joueur2: '',
  poule: ''
})

onMounted(async () => {
  try {
    const res = await playerAPI.getPlayers()
    players.value = res.data
  } catch (err) {
    console.error(err)
    alert("Impossible de récupérer la liste des identifiants des joueurs")
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

// Exemple de fonction de validation
async function handleValider() {
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
    await teamStore.createTeam(data)
    alert("L'équipe a bien été créée !")
    router.push('/equip')
  } catch (err) {
    console.error("Erreur détaillée:", err.response?.data || err.message)
    alert("Erreur lors de la création de l'équipe: " + (err.response?.data?.detail || err.message))
  }
}
</script>

<style scoped></style>