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
          <select
            v-model="form.user_id"
            class="w-full p-2 rounded border"
            required
          >
            <option disabled value="">-- Sélectionner un email --</option>
            <option
              v-for="user in users"
              :key="user.id"
              :value="user.id"
            >
              {{ user.email }}
            </option>
          </select>
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
import { playerAPI } from "@/services/api"
import { usePlayerStore } from "@/stores/player"
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

// Définir les données avec ref
const router = useRouter()
const store = usePlayerStore()

const users = ref([])

const form = ref({
  user_id: "",
  first_name: "",
  last_name: "",
  company: "",
  license_number: ""
})

// Récupérer les utilisateurs pour le select
onMounted(async () => {
  try {
    const response = await playerAPI.getUsersForSelect()
    users.value = response.data
  } catch (err) {
    console.error(err)
  }
})


// Exemple de fonction de validation
async function handleValider() {
  try {
    await store.createPlayer({ ...form.value })
    router.push("/players")
  } catch (err) {
    console.error(err)
    alert("Erreur lors de la création du joueur")
  }
}
</script>

<style scoped></style>
