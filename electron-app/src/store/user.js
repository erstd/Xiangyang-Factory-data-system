import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    username: localStorage.getItem('username') || '',
    role: localStorage.getItem('role') || '',
    token: localStorage.getItem('token') || ''
  }),

  actions: {
    setUser(userData) {
      this.username = userData.username;
      this.role = userData.role;
      this.token = userData.token;

      localStorage.setItem('username', userData.username);
      localStorage.setItem('role', userData.role);
      localStorage.setItem('token', userData.token);
    },

    clearUser() {
      this.username = '';
      this.role = '';
      this.token = '';

      localStorage.removeItem('username');
      localStorage.removeItem('role');
      localStorage.removeItem('token');
    }
  },

  getters: {
    isFinance: (state) => state.role === 'finance',
    isFactory: (state) => state.role === 'factory'
  }
});
