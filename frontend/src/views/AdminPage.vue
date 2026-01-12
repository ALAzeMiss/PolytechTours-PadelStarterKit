<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">

    <!-- Barre de nav -->
    <NavAdminBar/>
    
    <!-- Contenu principal -->

    

  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const handleUser = () => router.push('/user/create')
const handleEquipe = () => router.push('/equip/create')
</script>
