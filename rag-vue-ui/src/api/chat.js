import http from './http'

export function askQuestion(question) {
  return http.post('/chat/ask', { question })
}
