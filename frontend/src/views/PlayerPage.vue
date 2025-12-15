<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <!-- Contenu principal -->
    <div class="flex justify-between items-center mb-4 p-6">
      <h1 class="text-2xl font-bold">Liste des joueurs</h1>

      <!-- Bouton Ajouter -->
      <button @click="handlePlayer"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        ➕ Ajouter
      </button>
    </div>

    <div class="px-20">
      <table class="min-w-full table-auto bg-white border border-gray-300 rounded-lg shadow mx-2">
        <thead class="bg-light-100">
          <tr>
            <th class="py-2 px-4 border">ID</th>
            <th class="py-2 px-4 border">Nom</th>
            <th class="py-2 px-4 border">Prénom</th>
            <th class="py-2 px-4 border">Entreprise</th>
            <th class="py-2 px-4 border">N° de Licence</th>
            <th class="py-2 px-4 border">Email</th>
            <th class="py-2 px-4 border">Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="p in store.players" :key="p.id" class="hover:bg-gray-50">
            <td class="py-2 px-4 border">{{ p.id }}</td>
            <td class="py-2 px-4 border">{{ p.last_name }}</td>
            <td class="py-2 px-4 border">{{ p.first_name }}</td>
            <td class="py-2 px-4 border">{{ p.company }}</td>
            <td class="py-2 px-4 border">{{ p.license_number }}</td>
            <td class="py-2 px-4 border">{{ p.email }}</td>

            <!-- Actions: Modifier / Supprimer -->
            <td class="py-2 px-4 border flex gap-6 justify-center">
              <!-- Crayon pour modifier -->
              <router-link :to="`/players/edit/${p.id}`">✏️</router-link>
              <button @click="store.deletePlayer(p.id)">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Nombre total de joueurs -->
    <div class="p-6 text-right text-gray-700 font-semibold text-lg">
      Total joueurs : {{ store.players.length }}
    </div>

  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { usePlayerStore } from "@/stores/player"

const router = useRouter()
const store = usePlayerStore()

onMounted(() => {
  store.getPlayers()
})

const handlePlayer = () => router.push('/players/create')


</script>

<style scoped></style>