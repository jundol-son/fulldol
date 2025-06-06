<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-6">🤖 자동매매 전략 등록</h2>

    <!-- 매수/매도 선택 라디오 버튼 -->
    <div class="mb-4">
      <label class="mr-4">
        <input type="radio" value="buy" v-model="form.side" class="mr-1" @change="filterConditions" /> 🟢 매수 전략
      </label>
      <label>
        <input type="radio" value="sell" v-model="form.side" class="mr-1" @change="filterConditions" /> 🔴 매도 전략
      </label>
    </div>

    <!-- 등록 폼 -->
    <div class="grid grid-cols-2 gap-4 mb-8 p-4 border rounded bg-white shadow">
      <div>
        <label class="block mb-1">📈 종목 선택</label>
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
      </div>

      <div>
        <label class="block mb-1">⚙️ 조건 선택</label>
        <select v-model="form.condition_id" class="w-full p-2 border rounded" @change="applyCondition">
          <option disabled value="">조건을 선택하세요</option>
          <option v-for="cond in filteredConditions" :key="cond.id" :value="cond.id">
            {{ cond.name }} ({{ cond.key }})
          </option>
        </select>
      </div>

      <div class="col-span-2" v-if="selectedCondition">
        <div v-for="input in selectedCondition.inputs" :key="input.key">
          <label class="block mb-1 font-semibold">{{ input.label }}</label>
          <input
            v-model="form.condition_value[input.key]"
            :type="input.type"
            class="w-full border p-2 rounded"
            :required="input.required"
          />
        </div>
      </div>

      <div>
        <label class="block mb-1">🔢 수량</label>
        <input v-model.number="form.quantity" type="number" class="w-full p-2 border rounded" placeholder="예: 10" />
      </div>

      <div>
        <label class="block mb-1">💰 단가 (선택)</label>
        <input v-model.number="form.unit_price" type="number" class="w-full p-2 border rounded" placeholder="지정가가 없으면 현재가" />
      </div>

      <div class="flex items-center gap-2 mt-4">
        <input v-model="form.is_active" type="checkbox" />
        <label>활성화 유무</label>
      </div>

      <div class="col-span-2 mt-4">
        <button @click="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">전략 저장</button>
      </div>
    </div>

    <!-- 전략 리스트 -->
    <div>
      <h3 class="text-xl font-semibold mb-2">📋 등록된 전략</h3>
      <table class="w-full text-sm border">
        <thead class="bg-gray-100">
          <tr>
            <th class="p-2 border">종목</th>
            <th class="p-2 border">전략</th>
            <th class="p-2 border">조건</th>
            <th class="p-2 border">수량</th>
            <th class="p-2 border">단가</th>
            <th class="p-2 border">활성</th>
            <th class="p-2 border">결과</th>
            <th class="p-2 border">관리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in strategyList" :key="item.id">
            <td class="p-2 border">{{ item.name }}</td>
            <td class="p-2 border">{{ item.side === 'sell' ? '매도' : '매수' }}</td>
            <td class="p-2 border whitespace-pre-wrap text-left">
              <div><strong>key:</strong> {{ getConditionKey(item.condition_id) }}</div>
              <pre>{{ JSON.stringify(item.condition_value, null, 2) }}</pre>
            </td>
            <td class="p-2 border">{{ item.quantity }}</td>
            <td class="p-2 border">{{ item.unit_price || '현재가' }}</td>
            <td class="p-2 border">{{ item.is_active ? '✅' : '❌' }}</td>
            <td class="p-2 border">{{ item.last_executed || '-' }}</td>
            <td class="p-2 border space-x-2">
              <button @click="toggleActive(item)" class="text-xs px-2 py-1 border rounded bg-yellow-100 hover:bg-yellow-200">
                {{ item.is_active ? '비활성화' : '활성화' }}
              </button>
              <button @click="remove(item.id)" class="text-xs px-2 py-1 border rounded bg-red-100 hover:bg-red-200">
                삭제
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Vue3Select from 'vue3-select'
import 'vue3-select/dist/vue3-select.css'

const selectedOption = ref(null)
const options = ref([])
const isLoading = ref(false)
const strategyList = ref([])
const allConditions = ref([])
const filteredConditions = ref([])
const selectedCondition = ref(null)

const form = ref({
  code: '',
  name: '',
  side: 'buy',
  condition_id: '',
  condition_value: {},
  quantity: 0,
  unit_price: null,
  is_active: true
})

const getConditionKey = (condition_id) => {
  const cond = allConditions.value.find(c => c.id === condition_id)
  return cond?.key || '-'
}

const onSelectAndFetch = (selected) => {
  if (selected?.code) {
    form.value.code = selected.code
    form.value.name = selected.name
  } else {
    form.value.code = ''
    form.value.name = ''
  }
}

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
      market: item.Market || (item.Nation === 'KR' ? 'KRX' : 'NASD')
    }))
  } catch (err) {
    console.error('검색 실패', err)
  }
  isLoading.value = false
}

const fetchStrategies = async () => {
  const res = await axios.get('http://localhost:8000/auto-buy')
  strategyList.value = res.data
}

const fetchConditions = async () => {
  const res = await axios.get('http://localhost:8000/conditions')
  allConditions.value = res.data
  filterConditions()
}

const filterConditions = () => {
  filteredConditions.value = allConditions.value.filter(c => c.side === form.value.side)
  selectedCondition.value = null
  form.value.condition_id = ''
  form.value.condition_value = {}
}

const applyCondition = () => {
  const selected = allConditions.value.find(c => c.id === form.value.condition_id)
  selectedCondition.value = selected || null
  form.value.condition_value = {}
}

const submit = async () => {
  const { code, name, condition_id, condition_value, quantity } = form.value
  if (!code || !name || !condition_id || Object.keys(condition_value).length === 0 || !quantity) {
    alert('⚠️ 필수 입력값이 누락되었습니다.')
    return
  }
  await axios.post('http://localhost:8000/auto-buy', form.value)
  alert('전략이 저장되었습니다 ✅')
  form.value = {
    code: '',
    name: '',
    side: 'buy',
    condition_id: '',
    condition_value: {},
    quantity: 0,
    unit_price: null,
    is_active: true
  }
  selectedOption.value = null
  selectedCondition.value = null
  fetchStrategies()
}

const toggleActive = async (item) => {
  await axios.put(`http://localhost:8000/auto-buy/${item.id}`, {
    is_active: !item.is_active
  })
  fetchStrategies()
}

const remove = async (id) => {
  if (confirm('정말 삭제하시겠습니까?')) {
    await axios.delete(`http://localhost:8000/auto-buy/${id}`)
    fetchStrategies()
  }
}

onMounted(async () => {
  await fetchStrategies()
  await fetchConditions()
  try {
    await axios.get('http://localhost:8000/stock/search?query=samsung')
    console.log("📦 종목 캐시 프리로딩 완료")
  } catch (err) {
    console.error("❌ 종목 캐시 로딩 실패", err)
  }
})
</script>
