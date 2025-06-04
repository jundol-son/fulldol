<template>
  <div class="register-container">
    <h2>회원가입</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="username" placeholder="아이디" />
      <input v-model="password" type="password" placeholder="비밀번호" />
      <input v-model="email" placeholder="이메일 (선택)" />
      <button type="submit">회원가입</button>
    </form>
    <p v-if="msg">{{ msg }}</p>
    <!-- 🔁 회원가입 페이지로 이동하는 버튼 -->
    <p>계정이 이미 있으신신가요?
      <router-link to="/login">로그인</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'  // 🔑 이걸 추가해야 router를 쓸 수 있어!

const username = ref('')
const password = ref('')
const email = ref('')
const msg = ref('')

const router = useRouter()  // 🔑 router 인스턴스를 가져옴

const handleRegister = async () => {
  try {
    const response = await axios.post('http://localhost:8000/register', {
      username: username.value,
      password: password.value,
      email: email.value
    })
    router.push({
      path: '/login',
      query: { msg: '회원가입 성공! 로그인 해주세요.' }
    })
  } catch (err) {
    console.error('회원가입 실패:', err)
    msg.value = err.response?.data?.detail || '에러가 발생했습니다.'
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
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
