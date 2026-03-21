<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script setup>
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

const chartData = {
  labels: props.data.labels,
  datasets: props.data.datasets.map(ds => ({
    ...ds,
    tension: 0.4,
    fill: true,
    borderWidth: 2
  }))
}

const chartOptions = {
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
      beginAtZero: true,
      grid: {
        color: 'rgba(148, 163, 184, 0.1)'
      },
      ticks: {
        font: { family: 'Fira Code', size: 11 }
      }
    },
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: { family: 'Fira Code', size: 11 }
      }
    }
  }
}
</script>
