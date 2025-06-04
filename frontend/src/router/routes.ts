import Register from '../pages/Register.vue'
import Login from '../pages/Login.vue'
import Board from '../pages/Board.vue'
import Write from '../pages/Write.vue'
import PostDetail from '../pages/PostDetail.vue'
import EditPost from '../pages/EditPost.vue'
// import MyPage from '../pages/MyPage.vue' // 마이페이지 생길 경우

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/board', component: Board, meta: { requiresAuth: true }  },
  { path: '/write', component: Write, meta: { requiresAuth: true }  },
  { path: '/post/:id', component: PostDetail, meta: { requiresAuth: true }  },
  { path: '/edit/:id', name: 'edit', component: EditPost, meta: { requiresAuth: true }  },
  // { path: '/mypage', component: MyPage, meta: { requiresAuth: true }  },
]

export default routes