<template>
  <aside
    class="bg-gray-100 w-64 h-full shadow-md transition-transform duration-300 ease-in-out z-50"
    :class="{ '-translate-x-full': !sidebarOpen }"
  >
    <div class="p-6 text-lg font-semibold text-blue-800 border-b border-gray-300">
      📚 메뉴
    </div>
    <nav class="flex flex-col gap-4 p-6 text-sm text-gray-700">
      <RouterLink to="/board" class="hover:text-blue-500">📄 게시판</RouterLink>
      <RouterLink to="/write" class="hover:text-blue-500">✍️ 새 글 작성</RouterLink>
      <RouterLink to="/mypage" class="hover:text-blue-500">👤 마이페이지</RouterLink>
      <RouterLink to="/balance" class="hover:text-blue-500">👤 잔고</RouterLink>
      <RouterLink to="/trade" class="hover:text-blue-500">📈 매수/매도 페이지</RouterLink>
      <RouterLink to="/tradehistory" class="hover:text-blue-500">📊 거래 내역</RouterLink>
      <RouterLink to="/autobuy" class="hover:text-blue-500">🤖 자동매수</RouterLink>
      <RouterLink to="/autobuycondition" class="hover:text-blue-500">🛠️ 자동매수조건 관리</RouterLink>
    </nav>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const sidebarOpen = defineProps(['sidebarOpen'])  // 부모에서 전달받음

const isMobile = ref(false)
onMounted(() => {
  username.value = localStorage.getItem('username') || ''
})

const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 200px;
  height: 100%;
  background-color: #f1f5f9;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 14px;
  border-right: 1px solid #e2e8f0;
}
a, button {
  background: none;
  border: none;
  color: #1e293b;
  text-align: left;
  cursor: pointer;
  font-size: 15px;
}
a:hover, button:hover {
  font-weight: bold;
}
</style>
