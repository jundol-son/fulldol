<template>
  <header class="w-full h-16 bg-yellow-100 flex justify-between items-center px-6 shadow-md">
    <div class="flex items-center gap-2">
      <button @click="$emit('toggleSidebar')" class="text-xl">☰</button>
      <span class="font-bold text-blue-900 text-lg">📘 첫 번째 풀스택 블로그</span>
    </div>
    <div class="flex items-center gap-3 text-sm">
      <span class="text-gray-800">{{ username }}님 환영합니다.</span>
      <button @click="logout" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded">
        로그아웃
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')

onMounted(() => {
  username.value = localStorage.getItem('username') || '게스트'
})

const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>
