// ============================================
// FICHIER : frontend/src/services/api.js
// ============================================

import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Intercepteur pour ajouter le token JWT
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Intercepteur pour gérer les erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expiré ou invalide
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API d'authentification
export const authAPI = {
  login: (email, password) => 
    api.post('/auth/login', { email, password }),

  logout: () =>
    api.post('/auth/logout'),

  changePassword: (currentPassword, newPassword, confirmPassword) =>
    api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
      confirm_password: confirmPassword
    })
}

export const userAPI = {
  createUser: (userData) =>
    api.post('/users/users', userData),

  getUsers: () =>
    api.get(`/users/users`),

  getUser: (userId) =>
    api.get(`/users/users/${userId}`),

  updateUser: (userId, userData) =>
    api.put(`/users/users/${userId}`, userData),

  deleteUser: (userId) =>
    api.delete(`/users/users/${userId}`),

  regeneratePassword: () =>
    api.get('/users/users/generate-password'),

  getUsersForSelect: () =>
    api.get('/users/users/select')
}

export const matchAPI = {
  getMatches: (params) =>
    api.get('/matches', { params }),

  getMatch: (matchId) =>
    api.get(`/matches/${matchId}`),

  createMatch: (matchData) =>
    api.post('/matches', matchData),

  updateMatch: (matchId, matchData) =>
    api.patch(`/matches/${matchId}`, matchData),

  deleteMatch: (matchId) =>
    api.delete(`/matches/${matchId}`)
}

export const playerAPI = {
  getPlayers: () =>
    api.get("/players/players"),

  getPlayer: (id) =>
    api.get(`/players/players/${id}`),

  createPlayer: (data) =>
    api.post("/players/players", data),

  updatePlayer: (id, data) =>
    api.put(`/players/players/${id}`, data),

  deletePlayer: (id) =>
    api.delete(`/players/players/${id}`)
}


export default api