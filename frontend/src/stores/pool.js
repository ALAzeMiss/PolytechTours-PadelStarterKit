import { defineStore } from "pinia"
import { ref } from "vue"
import { poolAPI } from "@/services/api"

export const usePoolStore = defineStore("pool", () => {
  const pools = ref([])
  const loading = ref(false)

  async function getPools() {
    loading.value = true
    const res = await poolAPI.getPools()
    pools.value = res.data
    loading.value = false
    return res.data
  }

  async function getPool(id) {
    const res = await poolAPI.getPool(id)
    return res.data
  }

  async function updatePool(id, data) {
    const res = await poolAPI.updatePool(id, data)
    const index = pools.value.findIndex(p => p.id === id)
    if (index !== -1) pools.value[index] = res.data
    return res.data
  }

  async function deletePool(id) {
    await poolAPI.deletePool(id)
    pools.value = pools.value.filter(p => p.id !== id)
  }

  async function createPool(data) {
    const res = await poolAPI.createPool(data)
    pools.value.push(res.data)
    await getPools()
  }

  return {
    pools,
    loading,
    getPools,
    getPool,
    updatePool,
    deletePool,
    createPool
  }
})
