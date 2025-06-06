import Register from '../pages/Register.vue'
import Login from '../pages/Login.vue'
import Board from '../pages/Board.vue'
import Write from '../pages/Write.vue'
import PostDetail from '../pages/PostDetail.vue'
import EditPost from '../pages/EditPost.vue'
import Balance from '../pages/Balance.vue'
import TradePage from '../pages/TradePage.vue'
import TradeHistory from '../pages/TradeHistoryTable.vue'
import ChartTest from '@/pages/ChartTest.vue'
import AutoBuy from '@/pages/AutoBuypage.vue'
import AutoBuyCondition from '@/pages/AutoBuyCondition.vue'
// import MyPage from '../pages/MyPage.vue' // 마이페이지 생길 경우

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/board', component: Board, meta: { requiresAuth: true }  },
  { path: '/write', component: Write, meta: { requiresAuth: true }  },
  { path: '/post/:id', component: PostDetail, meta: { requiresAuth: true }  },
  { path: '/edit/:id', name: 'edit', component: EditPost, meta: { requiresAuth: true }  },
  { path: '/balance', component: Balance, meta: { requiresAuth: true }  },
  { path: '/trade', component: TradePage, meta: { requiresAuth: true }  },
  { path: '/tradehistory', component: TradeHistory, meta: { requiresAuth: true }  },
  { path: '/charttest', component: ChartTest, meta: { requiresAuth: true }  },
  { path: '/autobuy', component: AutoBuy, meta: { requiresAuth: true }  },
  { path: '/autobuycondition', component: AutoBuyCondition, meta: { requiresAuth: true }  },
  // { path: '/mypage', component: MyPage, meta: { requiresAuth: true }  },
]

export default routes