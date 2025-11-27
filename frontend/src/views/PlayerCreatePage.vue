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
          <input v-model="nom" type="text" class="w-full p-2 rounded border" placeholder="Votre nom" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Entreprise</label>
          <input v-model="entreprise" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'entreprise" />
        </div>


        <div>
          <label class="block mb-1 font-medium">N° Licence</label>
          <input v-model="licence" type="text" class="w-full p-2 rounded border" placeholder="Numéro de licence" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Email</label>
          <input v-model="email" type="email" class="w-full p-2 rounded border" placeholder="email@example.com" />
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
import { useRouter } from 'vue-router'

// Définir les données avec ref
import { ref } from 'vue'

const nom = ref('')
const entreprise = ref('')
const licence = ref('')
const email = ref('')

// Utiliser le router
const router = useRouter()

// Exemple de fonction de validation
function handleValider() {
  console.log('Formulaire :', nom.value, entreprise.value, licence.value, email.value)
  router.push('/player')
}
</script>



<style scoped></style>
