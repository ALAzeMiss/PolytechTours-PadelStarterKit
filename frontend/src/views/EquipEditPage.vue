<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <!-- Contenu principal centré -->
    <div class="flex flex-col items-center mt-10">

      <h1 class="text-3xl font-bold mb-8">
        Modifier l'équipe #{{ equipId }}
      </h1>

      <form
        @submit.prevent="updateEquip"
        class="bg-white shadow-lg rounded-xl p-8 w-full max-w-xl space-y-6"
      >
        <div>
          <label class="font-semibold">Entreprise</label>
          <input
            v-model="equip.entreprise"
            type="text"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">Nom Joueur 1</label>
          <input
            v-model="equip.joueur1"
            type="text"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">Nom Joueur 2</label>
          <input
            v-model="equip.joueur2"
            type="text"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">Poule</label>
          <input
            v-model="equip.poule"
            type="text"
            class="w-full p-2 rounded border bg-gray-100"
            disabled
          />
        </div>

        <button
          type="submit"
          class="w-full py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700"
        >
          Enregistrer
        </button>
      </form>

    </div>

  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const equipId = route.params.id

const equip = ref({
  entreprise: "",
  joueur1: "",
  joueur2: "",
  poule: ""
})

onMounted(async () => {
  // 🔥 Route corrigée
  const res = await fetch(`http://localhost:8000/equips/${equipId}`)

  if (!res.ok) {
    console.error("Erreur lors du chargement du joueur :", res.status)
    return
  }

  player.value = await res.json()
})

async function updateEquip() {
  const formData = new FormData()
  formData.append("entreprise", equip.value.entreprise)
  formData.append("joueur1", equip.value.joueur1)
  formData.append("joueur2", equip.value.joueur2)
  formData.append("poule", equip.value.poule)

  await fetch(`http://localhost:8000/equips/${equipId}`, {
    method: "PUT",
    body: formData
  })

  alert("Modifications enregistrées")
}
</script>

<style scoped>
</style>
