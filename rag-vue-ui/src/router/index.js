import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import ChatView from '../views/ChatView.vue'
import KnowledgeBaseView from '../views/KnowledgeBaseView.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView, meta: { public: true } },
  { path: '/chat', name: 'chat', component: ChatView },
  { path: '/knowledge-base', name: 'knowledgeBase', component: KnowledgeBaseView },
  { path: '/', redirect: '/chat' },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')
  if (!to.meta.public && !token) {
    return '/login'
  }
  if (to.path === '/login' && token) {
    return '/chat'
  }
  return true
})

export default router
