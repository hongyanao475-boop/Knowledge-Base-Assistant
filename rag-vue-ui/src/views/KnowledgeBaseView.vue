<template>
  <main class="kb-page">
    <header class="page-header">
      <div>
        <h1>Knowledge Base</h1>
        <p>Upload files, track indexing status, and keep each user's data isolated.</p>
      </div>
      <button @click="refreshAll" :disabled="loading">Refresh</button>
    </header>

    <section class="status-grid">
      <div class="metric">
        <span>Total documents</span>
        <strong>{{ status.document_count }}</strong>
      </div>
      <div class="metric">
        <span>Indexed</span>
        <strong>{{ status.indexed_count }}</strong>
      </div>
      <div class="metric">
        <span>Indexing</span>
        <strong>{{ status.indexing_count }}</strong>
      </div>
      <div class="metric">
        <span>Failed</span>
        <strong>{{ status.failed_count }}</strong>
      </div>
    </section>

    <section
      class="upload-panel"
      :class="{ dragging: isDragging }"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
    >
      <div>
        <h2>Upload document</h2>
        <p>Supported: TXT, Markdown, PDF, DOCX. The backend will index it asynchronously.</p>
      </div>
      <input ref="fileInput" type="file" accept=".txt,.md,.pdf,.docx" @change="onFileChange" />
      <button @click="uploadSelected" :disabled="uploading || !selectedFile">
        {{ uploading ? 'Uploading...' : 'Upload and index' }}
      </button>
      <span v-if="selectedFile" class="selected-file">{{ selectedFile.name }}</span>
    </section>

    <section class="document-panel">
      <div class="panel-title">
        <h2>Documents</h2>
        <span v-if="autoPolling">Auto refresh enabled while indexing</span>
      </div>

      <div v-if="loading" class="empty">Loading documents...</div>
      <div v-else-if="documents.length === 0" class="empty">No documents uploaded for this account.</div>
      <table v-else>
        <thead>
          <tr>
            <th>File</th>
            <th>Type</th>
            <th>Size</th>
            <th>Status</th>
            <th>Chunks</th>
            <th>Created</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doc in documents" :key="doc.id">
            <td>
              <div class="file-cell">
                <strong>{{ doc.filename }}</strong>
                <small v-if="doc.error_msg">{{ doc.error_msg }}</small>
              </div>
            </td>
            <td>{{ doc.file_type }}</td>
            <td>{{ formatSize(doc.file_size) }}</td>
            <td><span :class="['status', doc.status]">{{ doc.status }}</span></td>
            <td>{{ doc.chunk_count }}</td>
            <td>{{ formatDate(doc.created_at) }}</td>
            <td><button class="danger" @click="remove(doc.id)">Delete</button></td>
          </tr>
        </tbody>
      </table>
    </section>

    <p v-if="message" class="toast">{{ message }}</p>
  </main>
</template>

<script>
import { deleteDocument, getKnowledgeStatus, listDocuments, uploadDocument } from '@/api/document'

export default {
  name: 'KnowledgeBaseView',
  data() {
    return {
      loading: false,
      uploading: false,
      isDragging: false,
      selectedFile: null,
      message: '',
      pollTimer: null,
      status: {
        document_count: 0,
        indexed_count: 0,
        indexing_count: 0,
        failed_count: 0,
      },
      documents: [],
    }
  },
  computed: {
    autoPolling() {
      return this.documents.some((doc) => ['pending', 'indexing'].includes(doc.status))
    },
  },
  async created() {
    await this.refreshAll()
  },
  beforeUnmount() {
    this.stopPolling()
  },
  methods: {
    async refreshAll() {
      this.loading = true
      try {
        const [statusRes, docsRes] = await Promise.all([getKnowledgeStatus(), listDocuments()])
        this.status = statusRes.data
        this.documents = docsRes.data
        this.syncPolling()
      } catch (error) {
        this.message = error.response?.data?.detail || 'Failed to load knowledge base.'
      } finally {
        this.loading = false
      }
    },
    syncPolling() {
      if (this.autoPolling && !this.pollTimer) {
        this.pollTimer = window.setInterval(() => this.refreshAll(), 4000)
      }
      if (!this.autoPolling) {
        this.stopPolling()
      }
    },
    stopPolling() {
      if (this.pollTimer) {
        window.clearInterval(this.pollTimer)
        this.pollTimer = null
      }
    },
    onFileChange(event) {
      this.selectedFile = event.target.files?.[0] || null
    },
    handleDrop(event) {
      this.isDragging = false
      this.selectedFile = event.dataTransfer.files?.[0] || null
    },
    async uploadSelected() {
      if (!this.selectedFile) return
      this.uploading = true
      this.message = ''
      try {
        const res = await uploadDocument(this.selectedFile)
        this.message = `${res.data.filename} uploaded. Background indexing started.`
        this.selectedFile = null
        this.$refs.fileInput.value = ''
        await this.refreshAll()
      } catch (error) {
        this.message = error.response?.data?.detail || 'Upload failed.'
      } finally {
        this.uploading = false
      }
    },
    async remove(id) {
      if (!confirm('Delete this document?')) return
      try {
        await deleteDocument(id)
        this.message = 'Document deleted.'
        await this.refreshAll()
      } catch (error) {
        this.message = error.response?.data?.detail || 'Delete failed.'
      }
    },
    formatSize(size) {
      if (!size) return '0 B'
      if (size < 1024) return `${size} B`
      if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
      return `${(size / 1024 / 1024).toFixed(1)} MB`
    },
    formatDate(value) {
      if (!value) return '-'
      return new Date(value).toLocaleString()
    },
  },
}
</script>

<style scoped>
.kb-page {
  min-height: calc(100vh - 56px);
  padding: 24px 28px;
  background: #f4f7fb;
}

.page-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}

h1,
h2,
p {
  margin-top: 0;
}

h1 {
  font-size: 26px;
  color: #101828;
}

h2 {
  margin-bottom: 6px;
  font-size: 18px;
  color: #101828;
}

.page-header p,
.upload-panel p {
  color: #667085;
}

.page-header button,
.upload-panel button {
  height: 38px;
  padding: 0 14px;
  border-radius: 6px;
  background: #155eef;
  color: #fff;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin: 18px 0;
}

.metric {
  background: #fff;
  border: 1px solid #dfe5ee;
  border-radius: 8px;
  padding: 16px;
}

.metric span {
  display: block;
  color: #667085;
  font-size: 14px;
}

.metric strong {
  display: block;
  margin-top: 8px;
  font-size: 28px;
  color: #101828;
}

.upload-panel,
.document-panel {
  background: #fff;
  border: 1px solid #dfe5ee;
  border-radius: 8px;
  padding: 18px;
  margin-top: 16px;
}

.upload-panel {
  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: 12px;
}

.upload-panel.dragging {
  border-color: #155eef;
  background: #f5f8ff;
}

.selected-file {
  grid-column: 2 / 4;
  color: #475467;
  font-size: 13px;
}

.panel-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.panel-title span {
  color: #b54708;
  font-size: 13px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  text-align: left;
  padding: 12px;
  border-bottom: 1px solid #e4e7ec;
}

th {
  color: #475467;
  font-size: 14px;
}

.file-cell {
  display: grid;
  gap: 4px;
}

.file-cell small {
  color: #b42318;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  background: #eef2f7;
  font-size: 13px;
}

.status.indexed {
  color: #067647;
  background: #dcfae6;
}

.status.indexing,
.status.pending {
  color: #b54708;
  background: #fef0c7;
}

.status.failed {
  color: #b42318;
  background: #fee4e2;
}

.danger {
  padding: 6px 10px;
  border-radius: 6px;
  color: #b42318;
  background: #fee4e2;
}

.empty {
  padding: 24px;
  text-align: center;
  color: #667085;
}

.toast {
  margin-top: 14px;
  color: #155eef;
}
</style>
