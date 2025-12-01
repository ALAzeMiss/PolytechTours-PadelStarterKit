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
          <label class="font-semibold">Nom équipe 1</label>
          <input
            v-model="poule.equip1"
            type="text"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">Nom équipe 2</label>
          <input
            v-model="poule.equip2"
            type="text"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">Nom équipe 3</label>
          <input
            v-model="poule.equip3"
            type="text"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">Nom équipe 4</label>
          <input
            v-model="poule.equip4"
            type="text"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">Nom équipe 5</label>
          <input
            v-model="poule.equip5"
            type="text"
            class="w-full p-2 rounded border"
          />
        </div>

        <div>
          <label class="font-semibold">Nom équipe 6</label>
          <input
            v-model="poule.equip6"
            type="text"
            class="w-full p-2 rounded border"
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
const pouleId = route.params.id

const poule = ref({
  equip1: "",
  equip2: "",
  equip3: "",
  equip4: "",
  equip5: "",
  equip6: ""
})

onMounted(async () => {
  // 🔥 Route corrigée
  const res = await fetch(`http://localhost:8000/poules/${pouleId}`)

  if (!res.ok) {
    console.error("Erreur lors du chargement du joueur :", res.status)
    return
  }

  player.value = await res.json()
})

async function updatePoule() {
  const formData = new FormData()
  formData.append("equip1", poule.value.equip1)
  formData.append("equip2", poule.value.equip2)
  formData.append("equip3", poule.value.equip3)
  formData.append("equip4", poule.value.equip4)
  formData.append("equip5", poule.value.equip5)
  formData.append("equip6", poule.value.equip6)

  await fetch(`http://localhost:8000/poules/${pouleId}`, {
    method: "PUT",
    body: formData
  })

  alert("Modifications enregistrées")
}
</script>

<style scoped>
</style>
