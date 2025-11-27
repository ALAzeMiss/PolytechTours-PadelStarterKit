<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar />

    <div class="flex justify-between items-center mb-4 p-6">
      <h1 class="text-2xl font-bold">Liste des équipes</h1>

      <!-- Bouton Ajouter -->
      <button @click="handleEquip"
        class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        ➕ Ajouter
      </button>
    </div>

    <div class="px-20">
      <table class="min-w-full bg-white border border-blue-300 rounded-lg shadow mx-2">
        <thead class="bg-light-100">
          <tr>
            <th class="py-2 px-4 border">Entreprise</th>
            <th class="py-2 px-4 border">Joueur 1</th>
            <th class="py-2 px-4 border">Joueur 2</th>
            <th class="py-2 px-4 border">Poule</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="equip in equips" :key="equip.id" class="hover:bg-gray-50">
            <td class="py-2 px-4 border">{{ equip.id }}</td>
            <td class="py-2 px-4 border">{{ equip.name }}</td>
            <td class="py-2 px-4 border">{{ equip.entreprise }}</td>
            <td class="py-2 px-4 border">{{ equip.licenceNumber }}</td>
            <td class="py-2 px-4 border">{{ equip.email }}</td>

            <!-- Actions: Modifier / Supprimer -->
            <td class="py-2 px-4 border flex gap-6 justify-center">
              <!-- Crayon pour modifier -->
              <button @click="editEquip(equip.id)" class="text-blue-600 hover:text-blue-800 text-xl">
                ✏️
              </button>

              <!-- Poubelle pour supprimer -->
              <button @click="deleteEquip(equip.id)" class="text-red-600 hover:text-red-800 text-xl">
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>


  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const handleEquip = () => router.push('/equip/create')
</script>
