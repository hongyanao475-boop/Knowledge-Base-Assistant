<!-- components/DocumentList.vue -->
<template>
  <div class="document-list">
    <h3>已上传文档</h3>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <i class="fas fa-spinner fa-spin"></i> 加载中...
    </div>

    <!-- 错误提示 -->
    <div v-else-if="error" class="error-message">
      ❌ {{ error }}
    </div>

    <!-- 文档列表 -->
    <ul v-else-if="documents.length > 0" class="doc-items">
      <li
        v-for="doc in documents"
        :key="doc"
        class="doc-item"
      >
        <!-- 图标 + 文件名 -->
        <div class="doc-info">
          <i
            :class="getFileIcon(doc)"
            :style="{ color: getFileColor(doc) }"
          ></i>
          <span class="doc-name">{{ doc }}</span>
        </div>

        <!-- 删除按钮 -->
        <button
          @click="deleteDocument(doc)"
          :disabled="deleting === doc"
          class="btn btn-sm btn-outline-danger"
          title="删除文件"
        >
          <i class="fas fa-trash"></i>
        </button>
      </li>
    </ul>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      📄 暂无文档，快去上传吧！
    </div>
  </div>
</template>

<script>
export default {
  name: 'DocumentList',
  data() {
    return {
      documents: [],
      loading: false,
      error: null,
      deleting: null // 正在删除的文件名
    }
  },
  created() {
    this.fetchDocuments()
  },
  methods: {
    // 获取文档列表
    async fetchDocuments() {
      this.loading = true
      this.error = null
      try {
        const res = await fetch('/knowledge-base/documents')
        if (!res.ok) throw new Error('网络错误')
        const data = await res.json()
        this.documents = data.documents || []
      } catch (err) {
        this.error = '无法加载文档列表，请稍后重试'
        console.error('获取文档列表失败:', err)
      } finally {
        this.loading = false
      }
    },

    // 删除文档
    async deleteDocument(filename) {
      if (!confirm(`确定要删除 "${filename}" 吗？此操作不可恢复！`)) return

      this.deleting = filename
      try {
        const res = await fetch(`/knowledge-base/documents/${filename}`, {
          method: 'DELETE'
        })

        if (res.ok) {
          // 从本地列表移除
          this.documents = this.documents.filter(doc => doc !== filename)
          // 触发事件（可用于刷新状态）
          this.$emit('document-deleted', filename)
          this.$emit('show-toast', `✅ "${filename}" 已删除`)
        } else {
          const data = await res.json().catch(() => ({}))
          throw new Error(data.message || '删除失败')
        }
      } catch (err) {
        this.$emit('show-toast', `❌ 删除失败: ${err.message}`)
      } finally {
        this.deleting = null
      }
    },

    // 根据文件类型返回图标
    getFileIcon(filename) {
      const ext = filename.split('.').pop().toLowerCase()
      if (ext === 'pdf') return 'far fa-file-pdf'
      if (ext === 'txt') return 'far fa-file-alt'
      return 'far fa-file'
    },

    // 返回图标颜色
    getFileColor(filename) {
      const ext = filename.split('.').pop().toLowerCase()
      if (ext === 'pdf') return '#f00'
      if (ext === 'txt') return '#007bff'
      return '#666'
    }
  }
}
</script>

<style scoped>
.document-list {
  margin-top: 1rem;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.document-list h3 {
  margin-top: 0;
  color: #333;
  font-size: 1.2rem;
}

.loading,
.empty-state {
  text-align: center;
  color: #666;
  padding: 2rem 0;
  font-style: italic;
}

.error-message {
  color: #d32f2f;
  padding: 1rem;
  background-color: #ffebee;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.doc-items {
  list-style: none;
  padding: 0;
  margin: 0;
}

.doc-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.doc-item:hover {
  background-color: #f8f9fa;
}

.doc-info {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
}

.doc-name {
  font-size: 0.95rem;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.doc-item:last-child {
  border-bottom: none;
}

.btn i {
  margin: 0;
}
</style>