<template>
  <div class="p-4">
    <h2 class="text-2xl font-semibold mb-4">💰 매수/매도 주문</h2>

    <!-- 🔍 종목 검색 -->
    <label class="block mb-1">🔍 종목 검색</label>
    <Vue3Select
      v-model="selectedOption"
      :options="options"
      :filterable="false"
      :loading="isLoading"
      label="label"
      placeholder="종목명을 입력하세요"
      @update:modelValue="onSelectAndFetch"
      @search="onSearch"
    />

    <!-- 종목 정보 카드 -->
    <div v-if="stockCode" class="grid grid-cols-2 gap-4 mt-4 p-4 border rounded bg-white shadow text-sm">
      <!-- 왼쪽: 종목/현재가 -->
      <div class="space-y-1">
        <div class="flex items-center gap-2">
          <span>📌</span>
          <span><strong>종목:</strong> {{ stockName }} <span v-if="stockNation">[{{ stockNation }}]</span></span>
        </div>
        <div class="flex items-center gap-2">
          <span>✅</span>
          <span><strong>현재가:</strong> {{ marketInfo?.current_price || '-' }} {{ currencyPrefix }}</span>
        </div>
      </div>

      <!-- 오른쪽: 상태/응답 -->
      <div class="space-y-1">
        <div class="flex items-center gap-2">
          <span>📡</span>
          <span><strong>상태:</strong> {{ marketInfo?.message }}</span>
        </div>
        <div class="flex items-center gap-2">
          <span>📦</span>
          <span><strong>응답:</strong> {{ marketInfo?.status }}</span>
        </div>
      </div>
    </div>

    <!-- 📈 차트 영역 -->
    <div v-if="stockCode" class="col-span-2 text-center">
      <button
        @click="loadChart"
        class="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
      >
        📊 {{ stockName }} 차트 불러오기
      </button>
    </div>     
    <div v-if="chartVisible" class="mt-4">
      <ChartCandle :key="chartKey" :code="stockCode" />
    </div>

    <!-- 📥 주문 영역 -->
    <div v-if="marketInfo" class="mt-6 border-t pt-4">
      <h3 class="text-lg font-semibold mb-2">📥 주문 입력</h3>

      <div class="flex justify-between items-center mb-4">
        <p>📦 보유 수량: {{ ownedQty !== null ? ownedQty + ' 주' : '-' }}</p>
        <button
          @click="fetchBalance"
          class="bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded"
        >
          🔄 잔고 조회
        </button>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block mb-1">💰 매수 단가</label>
          <input v-model.number="price" type="number" class="w-full p-2 border rounded" placeholder="예: 95000" />
        </div>
        <div>
          <label class="block mb-1">🔢 수량</label>
          <input v-model.number="qty" type="number" class="w-full p-2 border rounded" placeholder="예: 10" />
        </div>
      </div>

      <div class="mt-4 flex gap-4">
        <button @click="placeOrder('buy')" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">🟢 매수</button>
        <button @click="placeOrder('sell')" class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">🔴 매도</button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Vue3Select from 'vue3-select'
import 'vue3-select/dist/vue3-select.css'
import ChartCandle from '@/components/ChartCandle.vue'

// 상태 선언
const selectedOption = ref(null)
const options = ref([])
const isLoading = ref(false)

const stockCode = ref('')
const chartVisible = ref(false)
const chartKey = ref(0)
const stockName = ref('')
const stockMarket = ref('')
const stockNation = ref('')

const marketInfo = ref(null)
const ownedQty = ref(null)
const price = ref(null)
const qty = ref(null)
const balanceList = ref([])

const loadChart = () => {
  chartVisible.value = true
  chartKey.value += 1  // 컴포넌트 강제 리렌더링
}

// ✅ 선택 시 시세 조회
const onSelectAndFetch = (selected) => {
  if (selected?.code) {
    stockCode.value = selected.code
    stockMarket.value = selected.market || ''
    stockName.value = selected.name
    stockNation.value = selected.nation
    marketInfo.value = null
    ownedQty.value = null
    chartVisible.value = false  // ✅ 새로운 종목 선택 시 차트 숨기기
    fetchMarketStatus()
  } else {
    stockCode.value = ''
    stockName.value = ''
    stockMarket.value = ''
    stockNation.value = ''
    marketInfo.value = null
    ownedQty.value = null
    chartVisible.value = false  // ✅ 새로운 종목 선택 시 차트 숨기기
  }
}

const currencyPrefix = computed(() => {
  if (stockNation.value === 'KR') return '₩'
  if (stockNation.value === 'US') return '$'
  return ''
})


// ✅ 입력할 때마다 서버 검색
const onSearch = async (query) => {
  if (!query) return
  isLoading.value = true
  try {
    const res = await axios.get(`http://localhost:8000/stock/search?query=${encodeURIComponent(query)}`)
    options.value = res.data.map(item => ({
      label: `${item.Name} (${item.Code}) [${item.Market || item.Nation}]`,
      code: item.Code,
      name: item.Name,
      nation: item.Nation,
      market: item.Market || (item.Nation === 'KR' ? 'KRX' : 'NASD')  // fallback
    }))
  } catch (err) {
    console.error('검색 실패', err)
  }
  isLoading.value = false
}

// 시세 조회
const fetchMarketStatus = async () => {
  if (!stockCode.value) return
  try {
    const res = await axios.get('http://localhost:8000/kis/market-status', {
      params: {
        code: stockCode.value,
        market: stockMarket.value
      }
    })
    marketInfo.value = res.data
  } catch (err) {
    console.error('시세 조회 실패', err)
    marketInfo.value = {
      message: '조회 실패',
      current_price: '-'
    }
  }
}

// 잔고 조회
const fetchBalance = async () => {
  try {
    const res = await axios.get('http://localhost:8000/kis/balance')
    balanceList.value = res.data.stocks || []
    const found = balanceList.value.find(item => item.pdno === stockCode.value)
    ownedQty.value = found ? parseInt(found.hldg_qty) : 0
  } catch (err) {
    alert('잔고 조회 실패')
    console.error(err)
  }
}

// 주문
const placeOrder = async (side) => {
  if (!stockCode.value || !price.value || !qty.value) {
    alert('⚠️ 종목 코드, 가격, 수량을 모두 입력하세요.')
    return
  }

  if (side === 'sell' && qty.value > (ownedQty.value || 0)) {
    alert(`❌ 매도 수량이 보유 수량을 초과했습니다. (보유: ${ownedQty.value || 0})`)
    return
  }

  try {
    const res = await axios.post('http://localhost:8000/kis/order', {
      code: stockCode.value,
      price: price.value,
      qty: qty.value,
      side
    })
    alert(`${side === 'buy' ? '매수' : '매도'} 주문 성공 ✅\n메시지: ${res.data.message}`)
  } catch (err) {
    alert('❌ 주문 실패')
    console.error(err)
  }
}


onMounted(async () => {
  try {
    // 최초 진입 시, 백엔드 캐시 warm-up 목적의 dummy 호출
    await axios.get('http://localhost:8000/stock/search?query=samsung')
    console.log("📦 종목 캐시 프리로딩 완료")
  } catch (err) {
    console.error("❌ 종목 캐시 로딩 실패", err)
  }
})

</script>
