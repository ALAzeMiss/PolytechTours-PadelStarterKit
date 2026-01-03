import { defineStore } from "pinia"
import { ref } from "vue"
import { playerAPI } from "@/services/api"

export const usePlayerStore = defineStore("player", () => {
  const players = ref([])
  const loading = ref(false)

  async function getPlayers() {
    loading.value = true
    const res = await playerAPI.getPlayers()
    players.value = res.data
    loading.value = false
    return res.data
  }

  async function getPlayer(id) {
    const res = await playerAPI.getPlayer(id)
    return res.data
  }

  async function updatePlayer(id, data) {
    const res = await playerAPI.updatePlayer(id, data)
    const index = players.value.findIndex(p => p.id === id)
    if (index !== -1) players.value[index] = res.data
    return res.data
  }

  async function deletePlayer(id) {
    await playerAPI.deletePlayer(id)
    players.value = players.value.filter(p => p.id !== id)
  }

  async function createPlayer(data) {
    const res = await playerAPI.createPlayer(data)
    players.value.push(res.data)
    await getPlayers()
  }

  return {
    players,
    loading,
    getPlayers,
    getPlayer,
    updatePlayer,
    deletePlayer,
    createPlayer
  }
})
