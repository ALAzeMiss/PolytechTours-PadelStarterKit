import { defineStore } from "pinia"
import { ref } from "vue"
import { teamAPI } from "@/services/api"

export const useTeamStore = defineStore("team", () => {
    const teams = ref([])
    const loading = ref(false)

    async function getTeams() {
        loading.value = true
        const res = await teamAPI.getTeams()
        teams.value = res.data  
        loading.value = false
        return res.data
    }

    async function getTeam(id) {
        const res = await teamAPI.getTeam(id)
        return res.data
    }

    async function updateTeam(id, data) {
        const res = await teamAPI.updateTeam(id, data)
        const index = teams.value.findIndex(t => t.id === id)
        if (index !== -1) teams.value[index] = res.data
        return res.data
    }

    async function deleteTeam(id) {
        await teamAPI.deleteTeam(id)
        teams.value = teams.value.filter(t => t.id !== id)
    }
    async function createTeam(data) {
        const res = await teamAPI.createTeam(data)
        teams.value.push(res.data)
        await getTeams()
    }

    return {
        teams,
        loading,
        getTeams,
        getTeam,
        updateTeam,
        deleteTeam,
        createTeam
    }
})