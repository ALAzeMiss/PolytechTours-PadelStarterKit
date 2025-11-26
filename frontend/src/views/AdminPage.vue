// ============================================
// FICHIER : frontend/src/views/AdminPage.vue
// ============================================
 
<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="w-full max-w-md">
      <div class="bg-white rounded-lg shadow-2xl p-8">
       
        <div>
        <button
        type="submit"
        
        class="w-full py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          <span>Nouveau joueur</span>
        </button>
        </div>
       
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const handleClick = () => {
    router.push('/user/create')
  };

</script>

 
