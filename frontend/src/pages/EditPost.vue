<template>
  <div class="edit-container">
    <h2>✏️ 글 수정</h2>
    <form @submit.prevent="updatePost">
      <input v-model="title" placeholder="제목" />
      <br><br/>
      <textarea v-model="content" placeholder="내용 작성..." />
      <br><br/>
      <button type="submit">수정 완료</button>
      <button @click="goBack">수정 취소</button>
      <button @click="goList">목록으로</button>
    </form>
    <p v-if="msg">{{ msg }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const title = ref('')
const content = ref('')
const writer = ref(localStorage.getItem('username') || '')
const msg = ref('')
const currentUser = localStorage.getItem('username') || ''
const postId = route.params.id

onMounted(async () => {
  const res = await axios.get(`http://localhost:8000/posts/${postId}`)
  title.value = res.data.title
  content.value = res.data.content
})

const updatePost = async () => {
  try {
    await axios.put(`http://localhost:8000/posts/${postId}`, {
      title: title.value,
      content: content.value,
      writer: currentUser
    })
    msg.value = '수정 완료! 상세 페이지로 이동합니다.'
    setTimeout(() => {
      router.push(`/post/${postId}`)
    }, 1000)
  } catch (err) {
    msg.value = err.response?.data?.detail || '수정 실패'
  }
}
const goBack = () => {
  router.push(`/post/${postId}`)
}
const goList = () => {
  router.push(`/Board`)
}
</script>

<style scoped>
.edit-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}
</style>
