<!-- App.vue -->
<template>
  <div class="flex h-screen">
    <!-- 사이드바 -->
    <Sidebar :sidebarOpen="sidebarOpen" v-if="showHeader"/>

    <!-- 전체 오른쪽 영역 -->
    <div class="flex-1 flex flex-col">
      <Header @toggleSidebar="sidebarOpen = !sidebarOpen" v-if="showHeader"/>

      <!-- 콘텐츠 영역 -->
      <main class="flex-1 overflow-y-auto px-8 py-6 bg-gray-50">
        <router-view />
      </main>

      <footer class="text-center text-sm text-gray-500 py-2">
        © 2025
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'

const route = useRoute()

const showHeader = computed(() => {
  // 로그인, 회원가입 페이지에서는 숨김
  return !['/login', '/register'].includes(route.path)
})
const sidebarOpen = ref(true)
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}
</script>

<style scoped>
.app-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-layout {
  display: flex;
  flex: 1;
}

.content-area {
  flex: 1;
  width: 100%;
  padding: 40px 60px;   /* 좌우 여백만 지정 */
  box-sizing: border-box;
}
</style>