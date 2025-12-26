<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <!-- Contenu principal -->
    <div class="p-6 max-w-xl mx-auto">
      <h1 class="text-2xl font-bold mb-6">Création d'un Joueur</h1>


      <form class="space-y-4">
        <div>
          <label class="block mb-1 font-medium">Nom</label>
          <input v-model="form.last_name" type="text" class="w-full p-2 rounded border" placeholder="Votre nom" />
        </div>

        <div>
          <label class="block mb-1 font-medium">Prénom</label>
          <input v-model="form.first_name" type="text" class="w-full p-2 rounded border" placeholder="Votre prénom" />
        </div>

        <div>
          <label class="block mb-1 font-medium">Entreprise</label>
          <input v-model="form.company" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'entreprise" />
        </div>


        <div>
          <label class="block mb-1 font-medium">N° Licence</label>
          <input v-model="form.license_number" type="text" class="w-full p-2 rounded border" placeholder="Numéro de licence" />
        </div>

        <!-- Email (USER) -->
        <div>
          <label class="block mb-1 font-medium">Utilisateur (email)</label>
          <input
            v-model="search"
            type="text"
            class="w-full p-2 rounded border"
            placeholder="Rechercher un email"
            @focus="showDropdown = true"
            @blur="hideDropdown"
          />
          <div v-if="showDropdown && filteredUsers.length" class="border rounded mt-1 max-h-40 overflow-y-auto bg-white">
            <div
              v-for="user in filteredUsers"
              :key="user.id"
              @mousedown="selectUser(user)"
              class="p-2 hover:bg-gray-100 cursor-pointer"
            >
              {{ user.email }}
            </div>
          </div>
        </div>
        
        <div class="flex justify-center">
          <button 
            @click="handleValider"
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
import { userAPI } from "@/services/api"
import { usePlayerStore } from "@/stores/player"
import { useRouter } from 'vue-router'
import { ref, onMounted, computed } from 'vue'

// Définir les données avec ref
const router = useRouter()
const store = usePlayerStore()

const users = ref([])
const search = ref('')
const showDropdown = ref(false)

const filteredUsers = computed(() => {
  if (!search.value) return users.value
  return users.value.filter(user => 
    user.email.toLowerCase().includes(search.value.toLowerCase())
  )
})

const form = ref({
  first_name: "",
  last_name: "",
  company: "",
  license_number: "",
  user_id: "", // L'id de l'utilisateur sélectionné
  birth_date: "",
  photo_url: ""
})
// Récupérer les utilisateurs pour le select
onMounted(async () => {
  try {
    const response = await userAPI.getUsersForSelect()
    users.value = response.data
  } catch (err) {
    console.error(err)
    alert("Impossible de récupérer les utilisateurs pour la sélection.")
  }
})

function selectUser(user) {
  form.value.user_id = user.id
  search.value = user.email
  showDropdown.value = false
}

function hideDropdown() {
  setTimeout(() => {
    showDropdown.value = false
  }, 150)
}


// Exemple de fonction de validation
async function handleValider() {
  if (!form.value.user_id) {
    alert("Veuillez sélectionner un utilisateur.")
    return
  }
  if (!form.value.first_name || !form.value.last_name || !form.value.company) {
    alert("Veuillez remplir le nom, le prénom et l'entreprise.")
    return
  }
  
  // Validation des regex
  const nameRegex = /^[a-zA-ZÀ-ÿ\s'-]{2,50}$/
  const companyRegex = /^[a-zA-ZÀ-ÿ0-9\s'-]{2,100}$/
  const licenseRegex = /^L\d{6}$/
  
  if (!nameRegex.test(form.value.first_name)) {
    alert("Le prénom doit contenir entre 2 et 50 caractères, uniquement des lettres, espaces, apostrophes ou tirets.")
    return
  }
  if (!nameRegex.test(form.value.last_name)) {
    alert("Le nom doit contenir entre 2 et 50 caractères, uniquement des lettres, espaces, apostrophes ou tirets.")
    return
  }
  if (!companyRegex.test(form.value.company)) {
    alert("L'entreprise doit contenir entre 2 et 100 caractères, uniquement des lettres, chiffres, espaces, apostrophes ou tirets.")
    return
  }
  if (form.value.license_number && !licenseRegex.test(form.value.license_number)) {
    alert("Le numéro de licence doit être au format L suivi de 6 chiffres (ex: L123456).")
    return
  }
  
  // Préparer les données en excluant les champs vides
  const data = { ...form.value }
  if (!data.birth_date) delete data.birth_date
  if (!data.photo_url) delete data.photo_url
  if (!data.license_number) delete data.license_number
  
  try {
    await store.createPlayer(data)
    alert("Le joueur " + form.value.first_name + " " + form.value.last_name + " a bien été créé !")
    router.push("/players")
  } catch (err) {
    console.error(err)
    alert("Erreur lors de la création du joueur")
  }
}
</script>

<style scoped></style>
