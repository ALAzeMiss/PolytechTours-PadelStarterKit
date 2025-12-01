<template>
  <nav class="bg-white shadow-md py-4 px-6 flex justify-center gap-8">
    
    <RouterLink 
      to="/player"
      class="text-lg font-semibold hover:text-blue-600"
      :class="{ 'text-blue-600 underline' : isActive('/player') }"
    >
      Joueurs
    </RouterLink>

    <RouterLink 
      to="/equip"
      class="text-lg font-semibold hover:text-blue-600"
      :class="{ 'text-blue-600 underline' : isActive('/equip') }"
    >
      Équipes
    </RouterLink>

    <RouterLink 
      to="/poule"
      class="text-lg font-semibold hover:text-blue-600"
      :class="{ 'text-blue-600 underline' : isActive('/poule') }"
    >
      Poules
    </RouterLink>

    <RouterLink 
      to="/users"
      class="text-lg font-semibold hover:text-blue-600"
      :class="{ 'text-blue-600 underline' : isActive('/users/create') }"
    >
      Comptes
    </RouterLink>

  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()

// met en surbrillance l'onglet actif
const isActive = (path) => route.path.startsWith(path)
</script>

<style scoped>
nav a {
  transition: 0.2s;
}
</style>
