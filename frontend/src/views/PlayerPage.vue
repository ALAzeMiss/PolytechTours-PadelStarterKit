<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <NavAdminBar />

    <div class="flex justify-between items-center mb-4 p-6">
      <h1 class="text-2xl font-bold">Liste des joueurs</h1>

      <!-- Bouton Ajouter -->
      <button 
        @click="handlePlayer"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        ➕ Ajouter
      </button>
    </div>

    <table class="min-w-full bg-white border border-gray-300 rounded-lg shadow mx-6">
      <thead class="bg-light-100">
        <tr>
          <th class="py-2 px-4 border">ID</th>
          <th class="py-2 px-4 border">Nom</th>
          <th class="py-2 px-4 border">Entreprise</th>
          <th class="py-2 px-4 border">N° de Licence</th>
          <th class="py-2 px-4 border">Email</th>
          <th class="py-2 px-4 border">Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr 
          v-for="user in users" 
          :key="user.id"
          class="hover:bg-gray-50"
        >
          <td class="py-2 px-4 border">{{ user.id }}</td>
          <td class="py-2 px-4 border">{{ user.name }}</td>
          <td class="py-2 px-4 border">{{ user.entreprise }}</td>
          <td class="py-2 px-4 border">{{ user.licenceNumber }}</td>
          <td class="py-2 px-4 border">{{ user.email }}</td>

          <!-- Actions: Modifier / Supprimer -->
          <td class="py-2 px-4 border flex gap-3 justify-center">
            <!-- Crayon pour modifier -->
            <button 
              @click="editPlayer(user.id)" 
              class="text-blue-600 hover:text-blue-800 text-xl"
            >
              ✏️
            </button>

            <!-- Poubelle pour supprimer -->
            <button 
              @click="deletePlayer(user.id)" 
              class="text-red-600 hover:text-red-800 text-xl"
            >
              🗑️
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Nombre total de joueurs -->
    <div class="p-6 text-right text-gray-700 font-semibold text-lg">
      Total joueurs : {{ users.length }}
    </div>

  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()

const users = ref([
  { id: 1, name: 'Alice', entreprise: 'Entreprise A', licenceNumber: '12345', email: 'alice@example.com', isAdmin: true },
  { id: 2, name: 'Bob', entreprise: 'Entreprise B', licenceNumber: '67890', email: 'bob@example.com', isAdmin: false }
])

const handlePlayer = () => router.push('/player/create')

const editPlayer = (id) => {
  router.push(`/player/edit/${id}`)
}

const deletePlayer = (id) => {
  users.value = users.value.filter(user => user.id !== id)
}
</script>

<style scoped></style>