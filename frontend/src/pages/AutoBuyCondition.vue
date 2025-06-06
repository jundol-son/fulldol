<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">🧩 조건 등록</h2>

    <div class="bg-white shadow p-4 rounded mb-6">
      <div class="mb-3">
        <label class="block font-semibold mb-1">조건 이름</label>
        <input v-model="form.name" class="w-full p-2 border rounded" placeholder="예: 골든크로스, 가격하락조건" />
      </div>
    <div class="mb-3">
      <label class="block font-semibold mb-1">조건 key</label>
      <input v-model="form.key" class="w-full p-2 border rounded" placeholder="예: limit_buy, gain_ratio" />
    </div>
      <div class="mb-3">
        <label class="block font-semibold mb-1">설명</label>
        <input v-model="form.description" class="w-full p-2 border rounded" placeholder="조건 설명" />
      </div>

      <div class="mb-3">
        <label class="block font-semibold mb-1">매수/매도</label>
        <div class="flex justify-center gap-6">
          <label><input type="radio" value="buy" v-model="form.side" /> 매수</label>
          <label><input type="radio" value="sell" v-model="form.side" /> 매도</label>
        </div>
      </div>  

      <div class="mb-3">
        <label class="block font-semibold mb-1">입력 필드</label>
        <div v-for="(field, idx) in inputFields" :key="idx" class="mb-2 flex gap-2 items-center">
          <input v-model="field.key" class="p-1 border rounded w-1/5" placeholder="key (예: price)" />
          <input v-model="field.label" class="p-1 border rounded w-1/3" placeholder="label (예: 지정가)" />
          <select v-model="field.type" class="p-1 border rounded w-1/5">
            <option value="text">text</option>
            <option value="number">number</option>
            <option value="date">date</option>
          </select>
          <label class="flex items-center gap-1 text-sm">
            <input type="checkbox" v-model="field.required" /> 필수
          </label>
          <button @click="removeInputField(idx)" class="text-red-500 hover:underline">삭제</button>
        </div>
        <button @click="addInputField" class="mt-2 bg-gray-200 px-2 py-1 rounded hover:bg-gray-300">+ 입력 필드 추가</button>
      </div>

      <div class="mt-4">
        <button @click="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">조건 저장</button>
      </div>
    </div>

    <div>
      <h3 class="text-xl font-semibold mb-2">📋 등록된 조건 목록</h3>
      <table class="w-full text-sm border">
        <thead class="bg-gray-100">
          <tr>
            <th class="p-2 border">이름</th>
            <th class="p-2 border">Key</th>
            <th class="p-2 border">설명</th>
            <th class="p-2 border">매수/매도</th>
            <th class="p-2 border">입력값</th>
            <th class="p-2 border">관리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in conditionList" :key="item.id">
            <td class="p-2 border">{{ item.name }}</td>
            <td class="p-2 border">{{ item.key }}</td>
            <td class="p-2 border">{{ item.description }}</td>
            <td class="p-2 border">{{ item.side }}</td>
            <td class="p-2 border whitespace-pre">{{ JSON.stringify(item.inputs, null, 2) }}</td>
            <td class="p-2 border text-center space-x-2">
              <button @click="edit(item)" class="text-blue-600 hover:underline">수정</button>
              <button @click="remove(item.id)" class="text-red-600 hover:underline">삭제</button>
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

const conditionList = ref([])
const form = ref({
  name: '',
  key: '',
  description: '',
  side: 'buy',
  inputs: []
})
const editingId = ref(null)
const inputFields = ref([{ key: '', label: '', type: 'text', required: false }])

const fetchConditions = async () => {
  const res = await axios.get('http://localhost:8000/conditions')
  conditionList.value = res.data
}

const addInputField = () => {
  inputFields.value.push({ key: '', label: '', type: 'text', required: false })
}

const removeInputField = (index) => {
  inputFields.value.splice(index, 1)
}

const submit = async () => {
  if (!form.value.name || !form.value.key || inputFields.value.some(f => !f.key || !f.label)) {
    alert('⚠️ 이름, key 및 입력 필드는 필수입니다.')
    return
  }
  form.value.inputs = inputFields.value

  if (editingId.value) {
    await axios.put(`http://localhost:8000/conditions/${editingId.value}`, form.value)
    alert('✅ 조건이 수정되었습니다.')
  } else {
    await axios.post('http://localhost:8000/conditions', form.value)
    alert('✅ 조건이 저장되었습니다.')
  }

  resetForm()
  fetchConditions()
}

const edit = (item) => {
  editingId.value = item.id
  form.value = {
    name: item.name,
    key: item.key,
    description: item.description,
    side: item.side,
    inputs: item.inputs || []
  }
  inputFields.value = [...form.value.inputs]
}

const remove = async (id) => {
  if (confirm('정말 삭제하시겠습니까?')) {
    await axios.delete(`http://localhost:8000/conditions/${id}`)
    fetchConditions()
  }
}

const resetForm = () => {
  editingId.value = null
  form.value = { name: '', key: '', description: '', side: 'buy', inputs: [] }
  inputFields.value = [{ key: '', label: '', type: 'text', required: false }]
}

onMounted(() => {
  fetchConditions()
})
</script>
