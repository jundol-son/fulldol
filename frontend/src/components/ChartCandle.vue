<!-- components/ChartCandle.vue -->
<template>
  <apexchart
    type="candlestick"
    height="350"
    :options="chartOptions"
    :series="series"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ApexCharts from 'vue3-apexcharts'

const props = defineProps({ code: String })

const series = ref([])
const chartOptions = ref({
  chart: { type: 'candlestick', height: 350 },
  xaxis: { type: 'category', labels: { rotate: -45 } },
  title: { text: '기간별 시세', align: 'left' }
})

onMounted(async () => {
  const res = await axios.get(`http://localhost:8000/kis/chart?code=${props.code}`)
  const response = res.data

  if (response.status !== 'ok') {
    console.error('❌ 차트 데이터 오류:', response)
    return
  }

  const candlesticks = response.data.map(item => ({
    x: item.Date.slice(0, 10),  // "YYYY-MM-DD"로 자르기
    y: [item.open, item.high, item.low, item.close]
  }))

  console.log("📊 변환된 캔들 데이터:", candlesticks)

  series.value = [{ data: candlesticks }]
})
</script>
