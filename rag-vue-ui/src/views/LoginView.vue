<template>
  <main class="auth-page">
    <section class="auth-panel">
      <div class="logo">R</div>
      <h1>RAGHub AI</h1>
      <p class="subtitle">Private knowledge base for RAG-powered Q&A</p>

      <div class="tabs">
        <button :class="{ active: mode === 'login' }" @click="mode = 'login'">Sign in</button>
        <button :class="{ active: mode === 'register' }" @click="mode = 'register'">Register</button>
      </div>

      <form @submit.prevent="submit">
        <label v-if="mode === 'register'">
          Email
          <input v-model.trim="form.email" type="email" autocomplete="email" />
        </label>
        <label>
          Username
          <input v-model.trim="form.username" autocomplete="username" />
        </label>
        <label>
          Password
          <input v-model="form.password" type="password" autocomplete="current-password" />
        </label>
        <button class="primary" :disabled="loading || !canSubmit">
          {{ loading ? 'Working...' : mode === 'login' ? 'Sign in' : 'Create account' }}
        </button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>
      <p class="hint">Tip: register a new account first, then upload documents.</p>
    </section>
  </main>
</template>

<script>
import { getMe, loginUser, registerUser } from '@/api/auth'

export default {
  name: 'LoginView',
  data() {
    return {
      mode: 'login',
      loading: false,
      error: '',
      form: {
        username: '',
        email: '',
        password: '',
      },
    }
  },
  computed: {
    canSubmit() {
      if (!this.form.username || !this.form.password) return false
      if (this.mode === 'register' && !this.form.email) return false
      return true
    },
  },
  methods: {
    async submit() {
      this.error = ''
      this.loading = true
      try {
        if (this.mode === 'register') {
          await registerUser(this.form)
        }
        const tokenRes = await loginUser({
          username: this.form.username,
          password: this.form.password,
        })
        localStorage.setItem('access_token', tokenRes.data.access_token)
        const me = await getMe()
        localStorage.setItem('current_user', JSON.stringify(me.data))
        this.$router.push('/chat')
      } catch (err) {
        this.error = err.response?.data?.detail || 'Request failed. Please check your input.'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: #f4f7fb;
}

.auth-panel {
  width: min(420px, calc(100vw - 32px));
  background: #fff;
  border: 1px solid #dfe5ee;
  border-radius: 8px;
  padding: 28px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
}

.logo {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  background: #155eef;
  color: white;
  font-weight: 800;
  margin-bottom: 14px;
}

h1 {
  margin: 0;
  font-size: 30px;
  color: #111827;
}

.subtitle {
  margin: 6px 0 20px;
  color: #667085;
}

.tabs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 18px;
}

.tabs button {
  height: 38px;
  border-radius: 6px;
  background: #eef2f7;
  color: #334155;
}

.tabs button.active {
  background: #155eef;
  color: #fff;
}

label {
  display: grid;
  gap: 6px;
  margin-bottom: 14px;
  color: #344054;
  font-size: 14px;
  text-align: left;
}

input {
  height: 40px;
  border: 1px solid #cfd7e3;
  border-radius: 6px;
  padding: 0 10px;
  font-size: 15px;
}

.primary {
  width: 100%;
  height: 42px;
  border-radius: 6px;
  background: #155eef;
  color: #fff;
}

.error {
  color: #b42318;
  margin-bottom: 0;
}

.hint {
  margin: 14px 0 0;
  color: #667085;
  font-size: 13px;
}
</style>
