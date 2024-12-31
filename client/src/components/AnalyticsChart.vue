<template>
    <div class="h-[300px]">
      <Chart type="doughnut" :data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue'
  import Chart from 'primevue/chart'
  import type { AnalyticsSummary } from '../types/Analytics'
  import { useAccountStore } from '../stores/accountStore'

  const accountStore = useAccountStore()

  const currencySymbol = accountStore.selectedCurrency?.symbol || ''
  
  interface Props {
    summary: AnalyticsSummary
  }
  
  const props = defineProps<Props>()
  
  const chartData = computed(() => {
    return {
      labels: props.summary.items.map(item => item.category),
      datasets: [{
        data: props.summary.items.map(item => item.total),
        backgroundColor: props.summary.items.map(item => item.color),
        hoverBackgroundColor: props.summary.items.map(item => item.color)
      }]
    }
  })

  const formatPercentage = (value: number, total: number): string => {
  const percentage = (value / total * 100).toFixed(1)
  return `${percentage}%`
}

  
  const chartOptions = {
    plugins: {
      legend: {
        display: false,        
      },
      tooltip: {
      callbacks: {
        label: (context) => {
          const value = context.raw as number
          const percentage = formatPercentage(value, props.summary.total)
          return [
            `${context.label}:`,
            `${currencySymbol + value} (${percentage})`
          ]
        }
      }
    }
  },
    responsive: true,
    maintainAspectRatio: true
  }
  </script>
  
  <style scoped>
  :deep(.p-chart) {
    height: 100%;
    display: flex;
    justify-content: center;
  }
  </style>