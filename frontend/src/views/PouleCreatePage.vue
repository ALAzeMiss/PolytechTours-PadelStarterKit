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
          <label class="block mb-1 font-medium">ID Poule</label>
          <input v-model="poolId" type="text" class="w-full p-2 rounded border" placeholder="ex: A, B, C" />
        </div>

        <div v-if="errorMsg" class="text-red-500 text-sm font-bold">
          {{ errorMsg }}
        </div>

        <div>
          <label class="block mb-1 font-medium">Équipe 1</label>
          <input v-model="equipe1" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 1" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Équipe 2</label>
          <input v-model="equipe2" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 2" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Équipe 3</label>
          <input v-model="equipe3" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 3" />
        </div>


        <div>
          <label class="block mb-1 font-medium">Équipe 4</label>
          <input v-model="equipe4" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 4" />
        </div>

        <div>
          <label class="block mb-1 font-medium">Équipe 5</label>
          <input v-model="equipe5" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 5" />
        </div>

        <div>
          <label class="block mb-1 font-medium">Équipe 6</label>
          <input v-model="equipe6" type="text" class="w-full p-2 rounded border" placeholder="Nom de l'équipe 6" />
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
import { ref } from 'vue'
import { poolAPI } from '@/services/api' // Import custom poolAPI

const poolId = ref('')
// Adding separate refs for teams to fix the bug, though not using them for DB creation yet
const equipe1 = ref('')
const equipe2 = ref('')
const equipe3 = ref('')
const equipe4 = ref('')
const equipe5 = ref('')
const equipe6 = ref('')

const errorMsg = ref('')

const router = useRouter()

async function handleValider() {
  errorMsg.value = ''
  if (!poolId.value) {
    errorMsg.value = "L'identifiant de la poule est requis."
    return
  }

  try {
    await poolAPI.createPool({ id: poolId.value })
    // TODO: Handle teams creation. Currently Team model requires linked Players.
    // We would need to search/select players or create dummy ones.
    // For now, only the Pool is created.
    console.log('Poule created:', poolId.value)
    router.push('/poule')
  } catch (err) {
    console.error("Erreur lors de la création de la poule", err)
    errorMsg.value = "Erreur lors de la création : " + (err.response?.data?.detail || err.message)
  }
}
</script>
