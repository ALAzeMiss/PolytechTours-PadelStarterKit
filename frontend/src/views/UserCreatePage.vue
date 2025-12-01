<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <NavAdminBar />

    <div class="max-w-6xl mx-auto p-10 grid grid-cols-1 md:grid-cols-2 gap-10">
      <!-- Colonne gauche : Création utilisateur -->
      <div class="bg-white p-8 rounded-2xl shadow-xl">
        <h2 class="text-3xl font-bold mb-6 text-gray-800">Liste des utilisateurs</h2>

        <ul class="space-y-3">
          <li v-for="user in users" :key="user.id" class="flex justify-between items-center p-3 border rounded-lg">
            <div>
              <p class="font-semibold">{{ user.email }}</p>
              <p class="text-sm text-gray-500">Role: {{ user.is_admin ? 'Admin' : 'Utilisateur' }}</p>
            </div>

            <button class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
              @click="regeneratePassword(user.id)">
              Nouveau mot de passe
            </button>
          </li>
        </ul>
      </div>

      <!-- Colonne droite : Liste utilisateurs -->

      <div class="bg-white p-8 rounded-2xl shadow-xl">
        <h2 class="text-3xl font-bold mb-6 text-gray-800">Créer un utilisateur</h2>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input v-model="email" type="email" placeholder="email@example.com"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" />
          </div>

          <label class="flex items-center space-x-2">
            <input type="checkbox" v-model="is_admin" />
            <span>Compte administrateur</span>
          </label>

          <button class="w-full py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            @click="handleCreateUser()">
            Ajouter un profil
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import NavAdminBar from '@/components/NavAdminBar.vue'
import { ref } from 'vue'
import { useUserStore } from '../stores/user.js'

// Champs pour création
const email = ref('')
const is_admin = ref(false)

const userStore = useUserStore()

// Exemple de liste utilisateurs
const users = ref([
  { id: 1, email: 'alice@example.com', is_admin: true },
  { id: 2, email: 'bob@example.com', is_admin: false }
])

const form = ref({
  email: '',
  is_admin: false
})

// Action sur bouton
const handleCreateUser = async () => {
  const result = await userStore.createUser(form.value)

  if (result.success) {
    users.value.push({
      id: result.userId,
      email: email.value,
      is_admin: is_admin.value
    })
  } else {
    alert('Erreur lors de la création de l\'utilisateur : ' + result.error)
  }

}

function regeneratePassword(userId) {
  console.log('Nouveau mot de passe généré pour', userId)
}
</script>


<style scoped></style>