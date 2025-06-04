<template>
  <div class="board-container">
    <h2>📋 게시판</h2>

    <!-- ✍️ 글쓰기 버튼 -->
    <br>
    <button @click="goWrite">글쓰기</button>
    
    <table>
      <thead>
        <tr>
          <th>번호</th>
          <th>제목</th>
          <th>작성자</th>
          <th>작성일</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="post in posts" :key="post.id">
          <td>{{ post.id }}</td>
          <td>  <router-link :to="`/post/${post.id}`">
                    {{ post.title }}
                </router-link>
          </td>
          <td>{{ post.writer }}</td>
          <td>{{ new Date(post.created_at).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
// 목데이터 (임시 글 목록)
const posts = ref([])
onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/posts')
    posts.value = response.data
  } catch (err) {
    console.error('글 불러오기 실패:', err)
  }
})
const goWrite = () => {
  router.push('/write')  // 글쓰기 페이지로 이동
}
</script>

<style scoped>
.board-container {
  margin: auto;
  padding: 20px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border-bottom: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}
</style>
