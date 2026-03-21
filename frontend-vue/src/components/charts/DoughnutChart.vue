<template>
  <Doughnut :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const chartData = {
  labels: props.data.labels,
  datasets: [{
    data: props.data.values,
    backgroundColor: [
      '#3B82F6',
      '#60A5FA',
      '#F97316',
      '#10B981',
      '#8B5CF6',
      '#EC4899'
    ],
    borderWidth: 0
  }]
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
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
  }
}
</script>
