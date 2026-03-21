<template>
  <Radar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Radar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const chartData = {
  labels: props.data.labels,
  datasets: props.data.datasets.map((ds, idx) => ({
    ...ds,
    backgroundColor: idx === 0 ? 'rgba(59, 130, 246, 0.2)' : 'rgba(249, 115, 22, 0.2)',
    borderColor: idx === 0 ? '#3B82F6' : '#F97316',
    borderWidth: 2,
    pointBackgroundColor: idx === 0 ? '#3B82F6' : '#F97316'
  }))
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
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
    r: {
      beginAtZero: false,
      min: 50,
      max: 100,
      ticks: {
        stepSize: 10,
        font: { family: 'Fira Code', size: 10 }
      },
      grid: {
        color: 'rgba(148, 163, 184, 0.2)'
      }
    }
  }
}
</script>
