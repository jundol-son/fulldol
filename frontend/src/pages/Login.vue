<template>
  <div class="login-container">
    <h2>풀스택 프로젝트</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="아이디" />
      <input v-model="password" type="password" placeholder="비밀번호" />
      <button type="submit">로그인</button>
    </form>

    <!-- 🔁 회원가입 페이지로 이동하는 버튼 -->
    <p>계정이 없으신가요?
      <router-link to="/register">회원가입</router-link>
    </p>

    <p v-if="msg">{{ msg }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const msg = ref(route.query.msg || '')

const username = ref('')
const password = ref('')


const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/login', {
      username: username.value,
      password: password.value
    })

    // ✅ localStorage에 로그인 정보 저장
    localStorage.setItem('username', response.data.username)

    msg.value = '로그인 성공!'
    setTimeout(() => {
      router.push('/board')
    }, 1000)
  } catch (err) {
    msg.value = err.response?.data?.detail || '로그인 실패'
  }
}

const logout = () => {
  localStorage.removeItem('username')
  router.push('/login')
}
</script>

<style scoped>
.login-container {
  margin: auto;
  padding: 20px;
}
input {
  display: block;
  margin: 10px 0;
  padding: 8px;
  width: 100%;
}
</style>
