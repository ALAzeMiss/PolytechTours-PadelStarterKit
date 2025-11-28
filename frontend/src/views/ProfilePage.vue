<template>
  <div class="min-h-screen bg-gray-100 p-10">
    <div class="max-w-xl mx-auto bg-white rounded-xl shadow-lg p-8">

      <h1 class="text-3xl font-bold mb-8 text-center">Profil utilisateur</h1>

      <!-- NOM -->
      <div class="mb-6">
        <label class="font-semibold">Nom</label>
        <input type="text" v-model="profile.nom" class="mt-1 w-full border px-3 py-2 rounded-lg" maxlength="50"
          minlength="2" />
      </div>

      <!-- PRENOM -->
      <div class="mb-6">
        <label class="font-semibold">Prénom</label>
        <input type="text" v-model="profile.prenom" class="mt-1 w-full border px-3 py-2 rounded-lg" maxlength="50"
          minlength="2" />
      </div>

      <!-- PHOTO DE PROFIL -->
      <div class="mb-6">
        <label class="font-semibold">Photo de profil</label>

        <div class="flex items-center gap-4 mt-2">
          <img :src="profile.photo" alt="Photo de profil" class="w-20 h-20 rounded-full object-cover border" />

          <div class="flex flex-col gap-2">
            <input type="file" accept="image/png, image/jpeg" @change="uploadPhoto" />
            <button v-if="profile.photo" @click="deletePhoto" class="text-red-600 hover:underline text-sm">
              Supprimer la photo
            </button>
          </div>
        </div>
      </div>

      <!-- DATE DE NAISSANCE -->
      <div class="mb-6">
        <label class="font-semibold">Date de naissance</label>
        <input type="date" v-model="profile.birthdate" class="mt-1 w-full border px-3 py-2 rounded-lg" />
      </div>

      <!-- EMAIL -->
      <div class="mb-6">
        <label class="font-semibold">Email</label>
        <input type="email" v-model="profile.email" class="mt-1 w-full border px-3 py-2 rounded-lg" />
      </div>

      <!-- NUMÉRO DE LICENCE (READ ONLY) -->
      <div class="mb-6">
        <label class="font-semibold">N° de licence (lecture seule)</label>
        <input type="text" :value="profile.licence"
          class="mt-1 w-full border px-3 py-2 rounded-lg bg-gray-100 cursor-not-allowed" readonly />
      </div>

      <!-- BOUTON SAUVEGARDER -->
      <button class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
        @click="saveProfile">
        Sauvegarder
      </button>

    </div>
  </div>
</template>


<script setup>
import { ref } from "vue"

const profile = ref({
  nom: "Dupont",
  prenom: "Marie",
  photo: "",
  birthdate: "1995-01-01",
  email: "marie.dupont@example.com",
  licence: "A12345678"
})

const uploadPhoto = (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 2 * 1024 * 1024) {
    alert("Image trop lourde (max 2 MB)")
    return
  }

  profile.value.photo = URL.createObjectURL(file)
}

const deletePhoto = () => {
  profile.value.photo = ""
}

const saveProfile = () => {
  console.log("Profil sauvegardé :", profile.value)
}
</script>