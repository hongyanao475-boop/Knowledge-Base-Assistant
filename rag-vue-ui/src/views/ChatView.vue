<template>
  <main class="chat-page">
    <header class="page-header">
      <div>
        <h1>AI Knowledge Chat</h1>
        <p>Ask questions against your private indexed documents.</p>
      </div>
      <router-link class="secondary-link" to="/knowledge-base">Manage documents</router-link>
    </header>
    <ChatInterface />
  </main>
</template>

<script>
import ChatInterface from '@/components/ChatInterface.vue'

export default {
  name: 'ChatView',
  components: { ChatInterface },
}
</script>

<style scoped>
.chat-page {
  min-height: calc(100vh - 56px);
  display: flex;
  flex-direction: column;
  background: #f4f7fb;
}

.page-header {
  padding: 20px 28px 12px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}

h1 {
  margin: 0;
  font-size: 26px;
  color: #101828;
}

p {
  margin: 6px 0 0;
  color: #667085;
}

.secondary-link {
  height: 38px;
  display: inline-flex;
  align-items: center;
  padding: 0 14px;
  border-radius: 6px;
  border: 1px solid #cfd7e3;
  background: #fff;
  color: #344054;
  text-decoration: none;
}
</style>
