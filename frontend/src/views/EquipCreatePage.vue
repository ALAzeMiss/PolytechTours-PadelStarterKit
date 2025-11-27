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
          <input v-model="nom" type="text" class="w-full p-2 rounded border" placeholder="Votre nom" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Joueur 1</label>
          <input v-model="joueur1" type="text" class="w-full p-2 rounded border" placeholder="Nom du joueur 1" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Joueur 2</label>
          <input v-model="joueur2" type="text" class="w-full p-2 rounded border" placeholder="Nom du joueur 2" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Poule</label>
          <input v-model="poule" type="text" class="w-full p-2 rounded border" placeholder="Nom de la poule" />
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

// Définir les données avec ref
import { ref } from 'vue'

const entreprise = ref('')
const joueur1 = ref('')
const joueur2 = ref('')
const poule = ref('')

// Utiliser le router
const router = useRouter()

// Exemple de fonction de validation
function handleValider() {
  console.log('Formulaire :', entreprise.value, joueur1.value, joueur2.value, poule.value)
  router.push('/equip')
}
</script>
