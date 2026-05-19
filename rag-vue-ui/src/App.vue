<template>
  <div id="app">
    <nav v-if="isAuthed" class="app-nav">
      <div class="brand">
        <span class="brand-mark">R</span>
        <span>RAGHub AI</span>
      </div>
      <router-link to="/chat">Chat</router-link>
      <router-link to="/knowledge-base">Knowledge Base</router-link>
      <div class="user-chip">{{ username }}</div>
      <button class="logout" @click="logout">Sign out</button>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    isAuthed() {
      return Boolean(localStorage.getItem('access_token')) && this.$route.path !== '/login'
    },
    username() {
      try {
        return JSON.parse(localStorage.getItem('current_user') || '{}').username || 'User'
      } catch {
        return 'User'
      }
    },
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('current_user')
      this.$router.push('/login')
    },
  },
}
</script>

<style scoped>
.app-nav {
  height: 56px;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 0 24px;
  background: #101828;
  color: #fff;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  margin-right: 12px;
}

.brand-mark {
  width: 28px;
  height: 28px;
  display: inline-grid;
  place-items: center;
  border-radius: 6px;
  background: #155eef;
}

a {
  color: #d0d5dd;
  text-decoration: none;
}

a.router-link-exact-active {
  color: #fff;
  font-weight: 700;
}

.user-chip {
  margin-left: auto;
  padding: 5px 10px;
  border-radius: 999px;
  background: #1d2939;
  color: #d0d5dd;
  font-size: 13px;
}

.logout {
  background: #344054;
  color: #fff;
  border-radius: 6px;
  padding: 8px 12px;
}
</style>
