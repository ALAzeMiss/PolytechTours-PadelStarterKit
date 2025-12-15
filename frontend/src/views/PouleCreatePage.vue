<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <!-- Contenu principal -->
    <div class="p-6 max-w-xl mx-auto">
      <h1 class="text-2xl font-bold mb-6">Création d'une poule</h1>
      <!-- Contenu principal -->
      <form class="space-y-4">
        <div>
          <label class="block mb-1 font-medium">Équipe 1</label>
          <input v-model="nom" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 1" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Équipe 2</label>
          <input v-model="joueur1" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 2" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Équipe 3</label>
          <input v-model="joueur2" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 3" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Équipe 4</label>
          <input v-model="poule" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 4" />
        </div>

        <div>
          <label class="block mb-1 font-medium">Équipe 5</label>
          <input v-model="poule" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 5" />
        </div>

        <div>
          <label class="block mb-1 font-medium">Équipe 6</label>
          <input v-model="poule" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 6" />
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

const equipe1 = ref('')
const equipe2 = ref('')
const equipe3 = ref('')
const equipe4 = ref('')
const equipe5 = ref('')
const equipe6 = ref('')

// Utiliser le router
const router = useRouter()

// Exemple de fonction de validation
function handleValider() {
  console.log('Formulaire :', equipe1.value, equipe2.value, equipe3.value, equipe4.value, equipe5.value, equipe6.value)
  router.push('/poule')
}
</script>
