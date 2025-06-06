<template>
  <div>
    <h2 class="text-xl mb-4">📊 거래 내역</h2>
    <input v-model="codeFilter" @input="fetchTrades" placeholder="종목 코드 입력" class="p-2 border rounded mb-2" />
    <table class="table-auto w-full border">
      <thead>
        <tr>
          <th>시간</th>
          <th>종목</th>
          <th>매수/매도</th>
          <th>수량</th>
          <th>단가</th>
          <th>총액</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="trade in trades" :key="trade.id">
          <td>{{ formatTime(trade.trade_time) }}</td>
          <td>{{ trade.code }}</td>
          <td>{{ trade.side }}</td>
          <td>{{ trade.qty }}</td>
          <td>{{ trade.price.toLocaleString() }}</td>
          <td>{{ trade.total_price.toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const trades = ref([])
const codeFilter = ref('')

const fetchTrades = async () => {
  const response = await axios.get('http://localhost:8000/kis/trade-history', {
    params: { code: codeFilter.value || undefined }
  })
  trades.value = response.data
}

// ✅ 여기에 정의하세요!
const formatTime = (utcString) => {
  const date = new Date(utcString);
  const koreaTime = new Date(date.getTime() + 9 * 60 * 60 * 1000);
  return koreaTime.toLocaleString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit"
  });
}

onMounted(fetchTrades)
</script>
