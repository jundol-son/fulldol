<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">📊 현재 잔고 요약</h1>

    <div v-if="loading">불러오는 중...</div>
    <div v-else-if="error" class="text-red-500">❌ 오류: {{ error }}</div>

    <div v-else>
      <!-- 잔고 요약 박스 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div v-for="(value, key) in displayBalance" :key="key" class="p-4 border rounded shadow bg-white">
          <div class="font-semibold text-gray-600">{{ labels[key] || key }}</div>
          <div class="text-lg font-bold text-blue-600">{{ formatNumber(value) }}</div>
        </div>
      </div>

      <!-- 종목별 보유 내역 테이블 -->
      <h2 class="text-xl font-semibold mb-2">📦 종목별 보유 내역</h2>
      <table class="min-w-full bg-white border">
        <thead>
          <tr class="bg-gray-100 text-left text-sm">
            <th class="px-4 py-2 border">종목코드</th>
            <th class="px-4 py-2 border">보유수량</th>
            <th class="px-4 py-2 border">평균매입가</th>
            <th class="px-4 py-2 border">현재가</th>
            <th class="px-4 py-2 border">평가손익</th>
            <th class="px-4 py-2 border">수익률</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stock in stockList" :key="stock.pdno" class="text-sm hover:bg-gray-50">
            <td class="px-4 py-2 border">{{ stock.pdno }}</td>
            <td class="px-4 py-2 border">{{ stock.hldg_qty}}</td>
            <td class="px-4 py-2 border">{{ formatNumber(stock.pchs_avg_pric) }}</td>
            <td class="px-4 py-2 border">{{ formatNumber(stock.prpr) }}</td>
            <td class="px-4 py-2 border">{{ formatNumber(stock.evlu_pfls_amt) }}</td>
            <td class="px-4 py-2 border">{{ stock.evlu_erng_rt }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const balance = ref(null)
const stockList = ref([])
const error = ref(null)
const loading = ref(true)

const labels = {
  tot_evlu_amt: "총 자산 평가액",
  dnca_tot_amt: "예수금",
  bfdy_buy_amt: "전일 매수금액",
  thdt_buy_amt: "당일 매수금액",
  thdt_sll_amt: "당일 매도금액",
  evlu_pfls_smtl_amt: "평가손익합계",
  asst_icdc_erng_rt: "자산 증감률 (%)",
}

const displayKeys = Object.keys(labels)
const displayBalance = ref({})

const formatNumber = (val) => {
  if (isNaN(val)) return val
  const num = parseFloat(val)
  return num.toLocaleString('ko-KR') + (val.includes('.') ? '' : ' ₩')
}

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/kis/balance')
    const data = res.data

    const summary = data.summary || {}
    displayKeys.forEach((key) => {
      displayBalance.value[key] = summary[key] || '0'
    })

    stockList.value = data.stocks || []
  } catch (e) {
    error.value = e.message || 'API 호출 실패'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
table {
  border-collapse: collapse;
}
th, td {
  text-align: center;
}
</style>
