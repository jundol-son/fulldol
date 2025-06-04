<!-- src/pages/Write.vue -->
<template>
  <div class="write-container">
    <h2>📝 글쓰기</h2>
    <form @submit.prevent="submitPost">
      <input v-model="title" placeholder="제목" />
      <textarea v-model="content" placeholder="내용 작성..." />
      <button type="submit">등록</button>
      <br><br/>
      <button @click="goBack">← 목록으로</button>
    </form>
    <p v-if="msg">{{ msg }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const title = ref('')
const content = ref('')
const writer = ref(localStorage.getItem('username') || '')
const msg = ref('')

const submitPost = async () => {
  try {
    const response = await axios.post('http://localhost:8000/posts', {
      title: title.value,
      content: content.value,
      writer: writer.value
    })

    msg.value = '✅ 글이 등록되었습니다!'
    setTimeout(() => {
      router.push('/board')
    }, 1000)
  } catch (err) {
    console.error('글쓰기 에러:', err)
    msg.value = err.response?.data?.detail || '❌ 오류가 발생했습니다.'
  }
}

const goBack = () => {
  router.push('/board')
}
</script>

<style scoped>
.write-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}
textarea {
  width: 100%;
  height: 150px;
  margin: 10px 0;
  padding: 10px;
}
</style>
