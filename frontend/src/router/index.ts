// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ✅ meta.requiresAuth 방식으로 로그인 여부 확인
router.beforeEach((to, from, next) => {
  const isLogin = !!localStorage.getItem('username')

  if (to.meta.requiresAuth && !isLogin) {
    alert('로그인이 필요합니다.')
    next('/login')
  } else {
    next()
  }
})

export default router
