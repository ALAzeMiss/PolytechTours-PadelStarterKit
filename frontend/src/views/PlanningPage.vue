// ============================================
// FICHIER : frontend/src/views/PlanningPage.vue
// ============================================

<template>
  <div class="min-h-screen flex items-start justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
    <div class="w-full max-w-5xl mx-auto p-6">
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <div class="p-6">
          <h2 class="text-xl font-semibold">PLANNING {{ monthYearLabel }}</h2>
          <div class="mt-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <button @click="prevMonth" class="px-3 py-1 bg-gray-100 rounded">&lt;</button>
              <div class="font-medium">{{ monthYearLabel }}</div>
              <button @click="nextMonth" class="px-3 py-1 bg-gray-100 rounded">&gt;</button>
            </div>
            <div class="text-sm text-gray-600">● = Événements planifiés</div>
          </div>

          <div class="mt-6 grid grid-cols-7 gap-2 text-center">
            <div class="font-medium text-sm text-gray-700" v-for="d in weekdays" :key="d">{{ d }}</div>
            <div v-for="(cell, idx) in calendarCells" :key="idx">
              <div
                class="p-3 h-20 border rounded flex flex-col items-center justify-start cursor-pointer"
                :class="{
                  'text-gray-400': !cell.inMonth,
                  'bg-blue-50 ring-2 ring-blue-300': isSameDate(cell.date, selectedDate),
                  'bg-blue-200': isToday(cell.date) && !isSameDate(cell.date, selectedDate)
                }"
                @click="selectDate(cell.date)"
              >
                <div class="w-full flex justify-center items-center gap-2">
                  <div class="text-sm font-medium">{{ cell.day }}</div>
                  <div v-if="hasEvents(cell.date)" class="ml-1 text-xs text-red-600">●</div>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-3 gap-6">
            <div class="col-span-2">
              <div class="text-sm font-semibold mb-2">DÉTAILS DU {{ selectedDateLabel }}</div>
              <div class="space-y-3">
                <div v-if="selectedEvents.length === 0" class="text-gray-600">Aucun événement programmé.</div>
                <div v-for="(ev, i) in selectedEvents" :key="i" class="border rounded p-3 bg-gray-50">
                  <div class="text-sm font-medium">{{ ev.time }} - {{ ev.location }}</div>
                  <div class="text-sm text-gray-700">{{ ev.title }}</div>
                </div>
              </div>
            </div>
            <div class="col-span-1">
              <div class="text-sm font-semibold mb-2">Légende</div>
              <div class="text-sm text-gray-700 space-y-2">
                <div class="flex items-center gap-2"><span class="text-red-600">●</span> Événements planifiés</div>
                <div class="flex items-center gap-2"><span class="w-3 h-3 bg-blue-200 inline-block rounded-full"></span> Aujourd'hui</div>
                <div class="flex items-center gap-2"><span class="w-3 h-3 border inline-block rounded"></span> Date sélectionnée</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// importations
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'

// accès au token de connexion
const authStore = useAuthStore()

const today = new Date()
const viewDate = ref(new Date(today.getFullYear(), today.getMonth(), 1))
const selectedDate = ref(new Date(today))

//-----------------------------------------------------------
// évennements en dur pour tester A SUPPRIMER
const events = ref([
  { date: '2025-11-15', time: '19:30', title: 'Tech Corp vs Innov Ltd', location: 'Piste 1' },
  { date: '2025-11-15', time: '18:00', title: 'Entraînement libre', location: 'Piste 2' },
  { date: '2025-11-22', time: '20:00', title: 'Match amical', location: 'Piste 3' },
  { date: '2025-11-09', time: '17:00', title: 'Tournoi junior', location: 'Piste 1' }
])
//-----------------------------------------------------------

// jours de la semaine pour l'en-tête du calendrier
const weekdays = ['L', 'M', 'M', 'J', 'V', 'S', 'D']

// formatage d'une date en 'YYYY-MM-DD' pour comparaison avec les événements
function formatYMD(d) {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

// affichage du mois et de l'année en cours 
const monthYearLabel = computed(() => {
  return viewDate.value.toLocaleString(undefined, { month: 'long', year: 'numeric' }).toUpperCase()
})

// obtention du premier jour affiché dans le calendrier (début de la semaine contenant le 1er du mois)
function startOfCalendar(dt) {
  const first = new Date(dt.getFullYear(), dt.getMonth(), 1)
  // getDay: 0 Sun .. 6 Sat. We want week starting Monday (L)
  let day = first.getDay() // 0..6 Sun..Sat
  // convert so Monday=0..Sunday=6
  day = (day + 6) % 7
  const start = new Date(first)
  start.setDate(first.getDate() - day)
  return start
}

// création des cellules du calendrier (28 - 31 cases du mois en cours + jours du mois précédent 
// et suivant pour compléter la grille en fonction de la disposition des semaines)
const calendarCells = computed(() => {
  const start = startOfCalendar(viewDate.value)
  const cells = []
  for (let i = 0; i < 42; i++) {
    const dt = new Date(start)
    dt.setDate(start.getDate() + i)
    cells.push({
      date: dt,
      day: dt.getDate(),
      inMonth: dt.getMonth() === viewDate.value.getMonth()
    })
  }
  return cells
})

// vérification si deux dates sont identiques (jour, mois, année)
function isSameDate(a, b) {
  if (!a || !b) return false
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate()
}

// vérification si la date d est aujourd'hui
function isToday(d) {
  return isSameDate(d, today)
}

// sélectionne la date d (click de l'utilisateur)
function selectDate(d) {
  selectedDate.value = new Date(d)
}

// aller au mois précédent
function prevMonth() {
  viewDate.value = new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() - 1, 1)
}

// aller au mois suivant
function nextMonth() {
  viewDate.value = new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() + 1, 1)
}

// vérification si la date d a des événements
function hasEvents(d) {
  return events.value.some(e => e.date === formatYMD(d))
}

// obtentention des événements pour la date d
function eventsFor(d) {
  return events.value.filter(e => e.date === formatYMD(d))
}

// affichage de la date sélectionnée en format lisible
const selectedDateLabel = computed(() => {
  if (!selectedDate.value) return ''
  return selectedDate.value.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }).toUpperCase()
})

// affichage des événements pour la date sélectionnée
const selectedEvents = computed(() => eventsFor(selectedDate.value))

//c'est déjà la fin :(
//<3
</script>