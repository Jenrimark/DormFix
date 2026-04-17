<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  Tooltip,
  Legend
)

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const RADAR_PALETTE = [
  { stroke: '#2563EB', fill: 'rgba(37, 99, 235, 0.18)' },   // blue
  { stroke: '#DC2626', fill: 'rgba(220, 38, 38, 0.18)' },   // red
  { stroke: '#16A34A', fill: 'rgba(22, 163, 74, 0.18)' },   // green
  { stroke: '#7C3AED', fill: 'rgba(124, 58, 237, 0.18)' },  // purple
  { stroke: '#EA580C', fill: 'rgba(234, 88, 12, 0.18)' },   // orange
  { stroke: '#0891B2', fill: 'rgba(8, 145, 178, 0.18)' },   // cyan
  { stroke: '#DB2777', fill: 'rgba(219, 39, 119, 0.18)' },  // pink
  { stroke: '#4B5563', fill: 'rgba(75, 85, 99, 0.18)' }     // slate
]

const chartData = computed(() => ({
  labels: props.data?.labels || [],
  datasets: (props.data?.datasets || []).map((ds, idx) => {
    const color = RADAR_PALETTE[idx % RADAR_PALETTE.length]
    return {
      ...ds,
      backgroundColor: color.fill.replace('0.18', '0.75'),
      borderColor: color.stroke,
      borderWidth: 1,
      borderRadius: 6,
      barPercentage: 0.8,
      categoryPercentage: 0.7
    }
  })
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false
  },
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
    y: {
      beginAtZero: true,
      min: 0,
      max: 100,
      ticks: {
        stepSize: 20,
        font: { family: 'Fira Code', size: 10 }
      },
      grid: {
        color: 'rgba(148, 163, 184, 0.2)'
      }
    },
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: { family: 'Fira Sans', size: 11 }
      }
    }
  }
}
</script>
