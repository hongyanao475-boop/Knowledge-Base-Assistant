<template>
  <div class="file-upload-component">
    <h3><i class="fas fa-upload"></i> 上传文件</h3>
    <p class="upload-tip">支持 .txt, .pdf, .docx, .pptx, .xlsx, .md 等格式</p>

    <!-- 隐藏的文件输入框 -->
    <input
      type="file"
      ref="fileInput"
      multiple
      @change="handleFileSelect"
      :disabled="disabled"
      style="display: none"
    />

    <!-- 选择文件按钮 -->
    <button
      @click="triggerFileInput"
      class="btn btn-upload"
      :disabled="disabled"
    >
      <i class="fas fa-folder-open"></i>
      {{ disabled ? '上传中...' : '选择文件' }}
    </button>

    <!-- 已选文件列表 -->
    <div v-if="localFiles.length > 0" class="selected-files">
      <h4>已选择 {{ localFiles.length }} 个文件：</h4>
      <ul>
        <li v-for="(file, index) in localFiles" :key="index">
          {{ file.name }} ({{ formatFileSize(file.size) }})
          <button @click="removeFile(index)" class="btn btn-sm btn-remove">×</button>
        </li>
      </ul>
      <!-- 将上传控制交给父组件 -->
      <slot name="upload-button" :start-upload="startUpload" :is-uploading="isUploading">
        <button @click="startUpload" class="btn btn-primary" :disabled="isUploading">
          {{ isUploading ? '上传中...' : '开始上传' }}
        </button>
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileUpload',
  props: {
    kbId: {
      type: Number,
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localFiles: [] // 本地暂存选中的文件
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      const files = Array.from(event.target.files);
      if (files.length === 0) return;

      const validFiles = files.filter(file => {
        const ext = file.name.toLowerCase().split('.').pop();
        return ['txt', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'md'].includes(ext);
      });

      if (validFiles.length !== files.length) {
        this.$emit('upload-error', new Error('部分不支持的文件类型已被过滤'));
      }

      this.localFiles = [...this.localFiles, ...validFiles];

      // 🚀 告诉父组件：文件已选好
      this.$emit('files-selected', this.localFiles);
    },
    removeFile(index) {
      this.localFiles.splice(index, 1);
      this.$emit('files-selected', this.localFiles);
    },
    startUpload() {
      // 🚀 告诉父组件：开始上传吧
      this.$emit('start-upload');
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
  }
};
</script>

<style scoped>
.file-upload-component {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.upload-tip {
  color: #666;
  font-size: 0.9em;
  margin-bottom: 1rem;
}

.btn-upload {
  background-color: #17a2b8;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-upload:hover:not(:disabled) {
  background-color: #138496;
}

.selected-files {
  margin-top: 1rem;
}

.selected-files ul {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}

.selected-files li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.btn-remove {
  background: #dc3545;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 1rem;
  line-height: 1;
  cursor: pointer;
  padding: 0;
}

.btn-remove:hover {
  background: #c82333;
}
</style>