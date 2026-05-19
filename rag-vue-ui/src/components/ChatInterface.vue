<template>
  <section class="chat-interface">
    <div class="toolbar">
      <div>
        <strong>RAG Chat</strong>
        <span>{{ messages.length }} messages</span>
      </div>
      <button @click="clearChat" :disabled="loading || messages.length === 0">Clear</button>
    </div>

    <div ref="messagesContainer" class="chat-messages">
      <div v-if="messages.length === 0" class="empty-state">
        <h2>Start with a question</h2>
        <p>The backend will retrieve relevant chunks from your own knowledge base before calling the LLM.</p>
        <div class="examples">
          <button v-for="item in examples" :key="item" @click="useExample(item)">{{ item }}</button>
        </div>
      </div>

      <article v-for="(msg, index) in messages" :key="index" :class="['message', msg.type]">
        <div class="bubble">
          <p>{{ msg.content }}</p>
          <span v-if="msg.cached" class="cache-badge">cache hit</span>
          <div v-if="msg.sources?.length" class="sources">
            <details open>
              <summary>Sources ({{ msg.sources.length }})</summary>
              <div v-for="(source, idx) in msg.sources" :key="idx" class="source-item">
                <div class="source-header">
                  <strong>{{ source.source }}</strong>
                  <span>score {{ Number(source.score).toFixed(4) }}</span>
                </div>
                <p>{{ truncate(source.content, 220) }}</p>
              </div>
            </details>
          </div>
        </div>
      </article>

      <article v-if="loading" class="message ai">
        <div class="bubble loading-bubble">
          <p>Retrieving knowledge chunks and generating answer...</p>
        </div>
      </article>
    </div>

    <form class="chat-input" @submit.prevent="sendMessage">
      <input
        v-model="inputMessage"
        :disabled="loading"
        placeholder="Ask a question about your uploaded documents"
      />
      <button :disabled="loading || !inputMessage.trim()">Send</button>
    </form>
  </section>
</template>

<script>
import { askQuestion } from '@/api/chat'

export default {
  name: 'ChatInterface',
  data() {
    return {
      messages: [],
      inputMessage: '',
      loading: false,
      examples: [
        'Summarize the key points of my documents.',
        'What problems are mentioned in the knowledge base?',
        'Give me an implementation checklist based on the documents.',
      ],
    }
  },
  methods: {
    useExample(text) {
      this.inputMessage = text
    },
    async sendMessage() {
      const question = this.inputMessage.trim()
      if (!question || this.loading) return

      this.messages.push({ type: 'user', content: question })
      this.inputMessage = ''
      this.loading = true

      try {
        const response = await askQuestion(question)
        this.messages.push({
          type: 'ai',
          content: response.data.answer,
          sources: response.data.sources || [],
          cached: response.data.cached,
        })
      } catch (error) {
        this.messages.push({
          type: 'ai',
          content: error.response?.data?.detail || 'Request failed. Please try again later.',
          sources: [],
        })
      } finally {
        this.loading = false
        this.$nextTick(this.scrollToBottom)
      }
    },
    clearChat() {
      this.messages = []
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) container.scrollTop = container.scrollHeight
    },
    truncate(text, length) {
      if (!text) return ''
      return text.length > length ? `${text.slice(0, length)}...` : text
    },
  },
}
</script>

<style scoped>
.chat-interface {
  flex: 1;
  margin: 0 28px 28px;
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid #dfe5ee;
  border-radius: 8px;
  overflow: hidden;
}

.toolbar {
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid #e4e7ec;
}

.toolbar span {
  margin-left: 8px;
  color: #667085;
  font-size: 13px;
}

.toolbar button {
  padding: 7px 10px;
  border-radius: 6px;
  background: #eef2f7;
  color: #344054;
}

.chat-messages {
  flex: 1;
  min-height: 420px;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.empty-state {
  margin: auto;
  max-width: 620px;
  text-align: center;
  color: #667085;
}

.empty-state h2 {
  margin: 0 0 8px;
  color: #101828;
  font-size: 22px;
}

.examples {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-top: 18px;
}

.examples button {
  padding: 8px 10px;
  border-radius: 6px;
  background: #f2f4f7;
  color: #344054;
}

.message {
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.ai {
  justify-content: flex-start;
}

.bubble {
  max-width: min(820px, 82%);
  border-radius: 8px;
  padding: 12px 14px;
  line-height: 1.6;
}

.message.user .bubble {
  color: #fff;
  background: #155eef;
}

.message.ai .bubble {
  color: #1f2937;
  background: #f8fafc;
  border: 1px solid #e4e7ec;
}

.bubble p {
  margin: 0;
  white-space: pre-wrap;
}

.cache-badge {
  display: inline-block;
  margin-top: 8px;
  padding: 2px 6px;
  border-radius: 4px;
  background: #dcfae6;
  color: #067647;
  font-size: 12px;
}

.sources {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px dashed #cfd7e3;
}

.source-item {
  margin-top: 10px;
  padding: 10px;
  border-radius: 6px;
  background: #fff;
  border: 1px solid #e4e7ec;
}

.source-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: #344054;
}

.source-header span {
  color: #667085;
  font-size: 13px;
}

.source-item p {
  margin-top: 6px;
  color: #475467;
  font-size: 14px;
}

.loading-bubble {
  color: #667085;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 14px;
  border-top: 1px solid #e4e7ec;
}

.chat-input input {
  flex: 1;
  height: 42px;
  border: 1px solid #cfd7e3;
  border-radius: 6px;
  padding: 0 12px;
}

.chat-input button {
  width: 88px;
  border-radius: 6px;
  background: #155eef;
  color: #fff;
}
</style>
