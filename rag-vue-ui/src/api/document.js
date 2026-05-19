import http from './http'

export function getKnowledgeStatus() {
  return http.get('/knowledge-bases/status')
}

export function listDocuments() {
  return http.get('/documents')
}

export function uploadDocument(file) {
  const formData = new FormData()
  formData.append('file', file)
  return http.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function deleteDocument(documentId) {
  return http.delete(`/documents/${documentId}`)
}
