<template>
  <div class="post-detail">
    <h2>📄 {{ post.title }}</h2>
    <p><strong>작성자:</strong> {{ post.writer }}</p>
    <p><strong>작성일:</strong> {{ new Date(post.created_at).toLocaleString() }}</p>
    <hr />
    <p>{{ post.content }}</p>
    <div v-if="post.writer === currentUser">
      <button @click="goEdit">✏️ 수정</button>
      <button @click="deletePost">❌ 삭제</button>
      <button @click="goBack">← 목록으로</button>
    </div>
    <div v-else>
      <button @click="goBack">← 목록으로</button>
    </div>
  </div>
    <!-- 조건부로 수정/삭제 버튼 노출 -->
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const post = ref({})
const postId = route.params.id
const currentUser = localStorage.getItem('username') || ''

const goEdit = () => {
  router.push(`/edit/${postId}`)
}

onMounted(async () => {
  try {
    const response = await axios.get(`http://localhost:8000/posts/${postId}`)
    post.value = response.data
  } catch (err) {
    alert('글을 불러오는 데 실패했습니다.')
    router.push('/board')
  }
})
const deletePost = async () => {
  if (!confirm('정말 삭제하시겠습니까?')) return

  try {
    await axios.delete(`http://localhost:8000/posts/${postId}`, {
      data: { writer: currentUser }  // ✅ 권한 확인용
    })
    alert('삭제되었습니다.')
    router.push('/board')
  } catch (err) {
    console.error('삭제 에러:', err)

    alert(
    '삭제 실패:\n' +
    (err.response?.data?.detail || err.message || JSON.stringify(err))
    )
  }
}
const goBack = () => {
  router.push('/board')
}
</script>

<style scoped>
.post-detail {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}
</style>
