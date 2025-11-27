<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar/>
    
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Liste des équipes</h1>

      <!-- Bouton Ajouter -->
      <button 
        @click="handleEquip"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        ➕ Ajouter
      </button>
    </div>

    <table class="min-w-full bg-white border border-blue-300 rounded-lg shadow">
      <thead class="bg-light-100">
        <tr>
          <th class="py-2 px-4 border">Entreprise</th>
          <th class="py-2 px-4 border">Joueur 1</th>
          <th class="py-2 px-4 border">Joueur 2</th>
          <th class="py-2 px-4 border">Poule</th>
        </tr>
      </thead>

      <tbody>
        <tr 
          v-for="player in players" 
          :key="player.id"
          class="hover:bg-gray-50"
        >
          <td class="py-2 px-4 border">{{ player.id }}</td>
          <td class="py-2 px-4 border">{{ player.name }}</td>
          <td class="py-2 px-4 border">{{ player.entreprise }}</td>
          <td class="py-2 px-4 border">{{ player.licenceNumber }}</td>
          <td class="py-2 px-4 border">{{ player.email }}</td>
        </tr>
      </tbody>
    </table>
    

  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const handleEquip = () => router.push('/equip/create')
</script>
