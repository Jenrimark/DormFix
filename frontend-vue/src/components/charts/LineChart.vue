<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const chartData = computed(() => ({
  labels: props.data?.labels || [],
  datasets: (props.data?.datasets || []).map(ds => ({
    ...ds,
    tension: 0.4,
    fill: true,
    borderWidth: 2,
    pointRadius: 3,
    pointHoverRadius: 5
  }))
}))

const yAxisValues = computed(() => {
  const values = (props.data?.datasets || [])
    .flatMap(ds => Array.isArray(ds?.data) ? ds.data : [])
    .map(v => Number(v))
    .filter(v => Number.isFinite(v))
  
  if (!values.length) {
    return {
      min: 0,
      max: 5,
      stepSize: 1
    }
  }

  const minValue = Math.min(...values)
  const maxValue = Math.max(...values)

  if (minValue === maxValue) {
    const baseline = Math.max(1, Math.ceil(maxValue * 0.2))
    return {
      min: Math.max(0, minValue - baseline),
      max: maxValue + baseline,
      stepSize: Math.max(1, Math.ceil((baseline * 2) / 5))
    }
  }

  const range = maxValue - minValue
  const paddedMin = Math.max(0, minValue - range * 0.1)
  const paddedMax = maxValue + range * 0.1
  const roughStep = (paddedMax - paddedMin) / 5
  const stepSize = Math.max(1, Math.ceil(roughStep))
  const min = Math.floor(paddedMin / stepSize) * stepSize
  const max = Math.ceil(paddedMax / stepSize) * stepSize

  return { min, max, stepSize }
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        font: { family: 'Fira Sans', size: 12 },
        usePointStyle: true,
        padding: 15
      }
    },
    tooltip: {
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      padding: 12,
      titleFont: { family: 'Fira Sans', size: 13 },
      bodyFont: { family: 'Fira Code', size: 12 }
    }
  },
  scales: {
    y: {
      beginAtZero: false,
      min: yAxisValues.value.min,
      max: yAxisValues.value.max,
      ticks: {
        stepSize: yAxisValues.value.stepSize,
        precision: 0,
        callback: (value) => Number.isInteger(value) ? value : ''
      },
      grid: {
        color: 'rgba(148, 163, 184, 0.1)'
      }
    },
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: { family: 'Fira Code', size: 11 },
        autoSkip: true,
        maxTicksLimit: 12
      }
    }
  }
}))
</script>
