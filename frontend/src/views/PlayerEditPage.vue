<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <!-- Contenu principal centré -->
    <div class="flex flex-col items-center mt-10">

      <h1 class="text-3xl font-bold mb-8">
        Modifier le joueur #{{ playerId }}
      </h1>

      <form
        @submit.prevent="updatePlayer"
        class="bg-white shadow-lg rounded-xl p-8 w-full max-w-xl space-y-6"
      >
        <div>
          <label class="font-semibold">Nom</label>
          <input
            v-model="player.name"
            type="text"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">Entreprise</label>
          <input
            v-model="player.entreprise"
            type="text"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">Email</label>
          <input
            v-model="player.email"
            type="email"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">N° de licence (lecture seule)</label>
          <input
            :value="player.licenceNumber"
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
const playerId = route.params.id

const player = ref({
  name: "",
  entreprise: "",
  email: "",
  licenceNumber: ""
})

onMounted(async () => {
  // 🔥 Route corrigée
  const res = await fetch(`http://localhost:8000/players/${playerId}`)

  if (!res.ok) {
    console.error("Erreur lors du chargement du joueur :", res.status)
    return
  }

  player.value = await res.json()
})

async function updatePlayer() {
  const formData = new FormData()
  formData.append("name", player.value.name)
  formData.append("entreprise", player.value.entreprise)
  formData.append("email", player.value.email)
  formData.append("licenceNumber", player.value.licenceNumber)

  await fetch(`http://localhost:8000/players/${playerId}`, {
    method: "PUT",
    body: formData
  })

  alert("Modifications enregistrées")
}
</script>

<style scoped>
</style>
