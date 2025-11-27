<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar/>
    
    <!-- Contenu principal -->
     <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Liste des poules</h1>

      <!-- Bouton Ajouter -->
      <button 
        @click="handlePoule"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        ➕ Ajouter
      </button>
    </div>
     <table class="min-w-full bg-white border border-gray-300 rounded-lg shadow">
      <thead class="bg-light-100">
        <tr>
          <th class="py-2 px-4 border">ID</th>
          <th class="py-2 px-4 border">Équipe</th>
        </tr>
      </thead>

      <tbody>
        <tr 
          v-for="player in players" 
          :key="player.id"
          class="hover:bg-gray-50"
        >
          <td class="py-2 px-4 border">{{ player.id }}</td>
          <td class="py-2 px-4 border">{{ player.team }}</td>
        </tr>
      </tbody>
    </table>

    

  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const handlePoule = () => router.push('/poule/create')
</script>
