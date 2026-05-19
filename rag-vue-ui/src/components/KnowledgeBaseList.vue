<template>
  <div class="kb-list-container">
    <h2>我的知识库</h2>
    <div v-if="knowledgeBases.length === 0" class="empty-state">
      <p>还没有创建任何知识库。点击上方按钮创建一个吧！</p>
    </div>
    <div v-else class="kb-grid">
      <div
        v-for="kb in knowledgeBases"
        :key="kb.id"
        class="kb-card"
        :class="{ 'selected': selectedKBId === kb.id }"
      >
        <div class="kb-card-header">
          <h3>{{ kb.name }}</h3>
          <div class="kb-actions">
            <button
              @click="$emit('upload-docs', kb)"
              class="btn btn-sm btn-outline-primary"
              title="上传文档"
            >
              <i class="fas fa-file-upload"></i>
            </button>
            <button
              @click="$emit('delete-kb', kb.id)"
              class="btn btn-sm btn-outline-danger"
              title="删除知识库"
            >
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
        <div class="kb-card-body">
          <p v-if="kb.description" class="kb-description">{{ kb.description }}</p>
          <p class="kb-info">
            <i class="fas fa-file-alt"></i> {{ kb.documentCount }} 个文档
            <span class="kb-date">
              <i class="far fa-calendar-alt"></i> {{ kb.createdAt }}
            </span>
          </p>
        </div>
        <div class="kb-card-footer">
          <button
            @click="$emit('select-kb', kb)"
            class="btn btn-sm btn-primary"
          >
            {{ selectedKBId === kb.id ? '已连接' : '连接' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KnowledgeBaseList',
  props: {
    knowledgeBases: {
      type: Array,
      required: true
    },
    selectedKBId: {
      type: Number,
      default: null
    }
  }
}
</script>

<style scoped>
.kb-list-container {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

.kb-list-container h2 {
  color: #333;
  margin-bottom: 1rem;
}

.empty-state {
  text-align: center;
  color: #666;
  padding: 2rem;
  background-color: #f1f3f5;
  border-radius: 8px;
}

.kb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.kb-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.kb-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.kb-card.selected {
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.kb-card-header {
  padding: 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.kb-card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.kb-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.btn-outline-primary {
  background: none;
  border: 1px solid #007bff;
  color: #007bff;
}

.btn-outline-primary:hover {
  background-color: #007bff;
  color: white;
}

.btn-outline-danger {
  background: none;
  border: 1px solid #dc3545;
  color: #dc3545;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
}

.kb-card-body {
  padding: 1rem;
}

.kb-description {
  color: #555;
  margin: 0 0 0.5rem 0;
  font-style: italic;
}

.kb-info {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.kb-info i {
  margin-right: 0.25rem;
}

.kb-date {
  margin-left: 1rem;
  color: #888;
}

.kb-card-footer {
  padding: 0.75rem 1rem;
  background-color: #f8f9fa;
  border-top: 1px solid #e0e0e0;
  text-align: right;
}
</style>