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
            <div class="flex items-center gap-4">
              <div class="text-sm text-gray-600">● = Événements planifiés</div>
              <!-- Toggle visible only for non-admin users -->
              <div v-if="!authStore.isAdmin" class="text-sm">
                <button
                  :class="viewMode === 'my' ? 'px-3 py-1 bg-blue-600 text-white rounded' : 'px-3 py-1 bg-gray-100 rounded'"
                  @click="setViewMode('my')">
                  Mes matchs
                </button>
                <button
                  :class="viewMode === 'all' ? 'px-3 py-1 bg-blue-600 text-white rounded' : 'px-3 py-1 bg-gray-100 rounded'"
                  @click="setViewMode('all')">
                  Tous
                </button>
              </div>
              <!-- For admins, show badge indicating 'Tous' -->
              <div v-else class="text-sm text-gray-600">Affichage: Tous</div>
            </div>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

// accès au token de connexion
const authStore = useAuthStore()

const today = new Date()
const viewDate = ref(new Date(today.getFullYear(), today.getMonth(), 1))
const selectedDate = ref(new Date(today))
// viewMode: 'my' (default for regular users) or 'all' (shows everyone)
const viewMode = ref('my')

//-----------------------------------------------------------
// événements récupérés depuis le backend
const events = ref([])
const datesWithEvents = ref(new Set())
const selectedEventsList = ref([])
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
  loadDayDetails(d)
}

// aller au mois précédent
function prevMonth() {
  viewDate.value = new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() - 1, 1)
  loadEventsRange()
}

// aller au mois suivant
function nextMonth() {
  viewDate.value = new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() + 1, 1)
  loadEventsRange()
}

// vérification si la date d a des événements
function hasEvents(d) {
  return datesWithEvents.value.has(formatYMD(d))
}

// obtention des événements pour la date d (utilise le détail chargé)
function eventsFor(d) {
  return selectedEventsList.value
}

// affichage de la date sélectionnée en format lisible
const selectedDateLabel = computed(() => {
  if (!selectedDate.value) return ''
  return selectedDate.value.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }).toUpperCase()
})

// affichage des événements pour la date sélectionnée
const selectedEvents = computed(() => eventsFor(selectedDate.value))

// Récupère la liste d'événements / matchs dans l'intervalle affiché
async function loadEventsRange() {
  const cells = calendarCells.value
  if (!cells.length) return
  const start = formatYMD(cells[0].date)
  const end = formatYMD(cells[cells.length - 1].date)

  try {
    if (viewMode.value === 'all') {
      const resp = await api.get('/events', { params: { start, end } })
      const data = resp.data
      // data is list of events; mark dates that have events
      const s = new Set()
      for (const ev of data) {
        // N'afficher la pastille que si au moins un match est présent
        if (ev.event_date && Array.isArray(ev.matches) && ev.matches.length > 0) {
          s.add(ev.event_date)
        }
      }
      datesWithEvents.value = s
    } else {
      // my mode: request user's matches and mark their event dates
      await loadMyEvents()
    }
  } catch (err) {
    console.error('Erreur loadEventsRange', err)
    // If unauthorized or other error, try loadMyEvents as fallback
    if (err?.response?.status === 401 || err?.response?.status === 403) {
      await loadMyEvents()
    }
  }
}

// Récupère les détails (matchs) pour une date sélectionnée
async function loadDayDetails(d) {
  const day = formatYMD(d)
  try {
    if (viewMode.value === 'all') {
      const resp = await api.get(`/events/day/${day}`)
      const payload = resp.data
      // Mapper les matchs en structure simple pour l'affichage
      const list = (payload.matches || []).map(m => ({
        time: m.event_time || '',
        title: `${m.team1?.company || 'Equipe 1'} vs ${m.team2?.company || 'Equipe 2'}`,
        location: m.court_number ? `Piste ${m.court_number}` : ''
      }))
      selectedEventsList.value = list
    } else {
      // my mode: fetch user's matches and filter by date
      const resp = await api.get('/events/my-events')
      const payload = resp.data
      const list = (payload.matches || []).filter(m => {
        const ed = m.event_date || m.event_date // ensure presence
        return ed === day
      }).map(m => ({
        time: m.event_time || '',
        title: `${m.team1?.company || 'Equipe 1'} vs ${m.team2?.company || 'Equipe 2'}`,
        location: m.court_number ? `Piste ${m.court_number}` : ''
      }))
      selectedEventsList.value = list
    }
  } catch (err) {
    console.error('Erreur loadDayDetails', err)
    selectedEventsList.value = []
  }
}

// Récupère les matchs de l'utilisateur connecté et marque les dates
async function loadMyEvents() {
  try {
    const resp = await api.get('/events/my-events')
    const payload = resp.data
    // payload.matches -> déterminer les dates depuis event_date
    // NOTE: reset the set so we don't keep previous "all" dates when switching to 'my'
    const s = new Set()
    for (const m of payload.matches || []) {
      if (m.event_date) s.add(m.event_date)
    }
    datesWithEvents.value = s
    // si la date sélectionnée correspond à un des matchs, charger les détails
    const sel = formatYMD(selectedDate.value)
    if (s.has(sel)) {
      await loadDayDetails(selectedDate.value)
    }
  } catch (err) {
    console.error('Erreur loadMyEvents', err)
  }
}

onMounted(() => {
  try { authStore.checkAuth() } catch (e) {}
  // Default view mode: admins see all, normal users see their matches
  viewMode.value = authStore.isAdmin ? 'all' : 'my'
  loadEventsRange()
  loadDayDetails(selectedDate.value)
})

watch(viewDate, () => {
  loadEventsRange()
})

function setViewMode(mode) {
  // only allow regular users to toggle; admins forced to 'all'
  if (authStore.isAdmin) {
    viewMode.value = 'all'
  } else {
    viewMode.value = mode
  }
  // reload calendar and selected day details
  loadEventsRange()
  loadDayDetails(selectedDate.value)
}

//c'est déjà la fin :(
//<3
</script>