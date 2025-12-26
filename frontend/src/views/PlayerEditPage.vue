<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Barre de nav -->
    <NavAdminBar />

    <!-- Contenu principal -->
    <div class="p-6 max-w-xl mx-auto">
      <h1 class="text-2xl font-bold mb-6">Modifier le joueur</h1>

      <form class="space-y-4">
        <div>
          <label class="block mb-1 font-medium">Nom</label>
          <input v-model="form.last_name" type="text" class="w-full p-2 rounded border" />
        </div>

        <div>
          <label class="block mb-1 font-medium">Prénom</label>
          <input v-model="form.first_name" type="text" class="w-full p-2 rounded border" />
        </div>

        <div>
          <label class="block mb-1 font-medium">Entreprise</label>
          <input v-model="form.company" type="text" class="w-full p-2 rounded border" />
        </div>

        <div>
          <label class="block mb-1 font-medium">N° Licence (lecture seule)</label>
          <input v-model="form.license_number" type="text" class="w-full p-2 rounded border bg-gray-100" disabled />
        </div>

        <div>
          <label class="block mb-1 font-medium">Email</label>
          <input v-model="form.email" type="email" class="w-full p-2 rounded border" />
        </div>

        <div class="flex justify-center">
          <button 
            @click.prevent="updatePlayer"
            class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition">
            Valider
          </button>
        </div>
      </form>
    </div>
  </div>
</template>


<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { ref, onMounted } from 'vue'
import { playerAPI } from "@/services/api"
import { usePlayerStore } from '@/stores/player'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()  
const playerId = route.params.id
const store = usePlayerStore()

const form = ref({
  first_name: "",
  last_name: "",
  company: "",
  license_number: "",
  email: "",
  birth_date: "",
  photo_url: ""
})

// Récupérer le joueur depuis le backend
onMounted(async () => {
  try {
    const res = await store.getPlayer(playerId)
    form.value = { ...res } // remplit automatiquement le formulaire
  } catch (err) {
    console.error(err)
    alert("Impossible de récupérer les informations du joueur")
  }
})

async function updatePlayer() {
  if (!form.value.first_name || !form.value.last_name || !form.value.company) {
    alert("Veuillez remplir le nom, le prénom et l'entreprise.")
    return
  }
  
  // Validation des regex
  const nameRegex = /^[a-zA-ZÀ-ÿ\s'-]{2,50}$/
  const companyRegex = /^[a-zA-ZÀ-ÿ0-9\s'-]{2,100}$/
  
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
  
  try {
    await store.updatePlayer(playerId, { ...form.value })
    alert("Modifications enregistrées")
    router.push("/players")
  } catch (err) {
    console.error(err)
    alert("Erreur lors de la mise à jour du joueur")
  }
}
</script>

<style scoped>
</style>
