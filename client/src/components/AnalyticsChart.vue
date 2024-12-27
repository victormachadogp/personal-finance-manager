<template>
    <div class="h-[300px]">
      <Chart type="doughnut" :data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue'
  import Chart from 'primevue/chart'
  import type { AnalyticsSummary } from '../types/Analytics'
  
  interface Props {
    summary: AnalyticsSummary
  }
  
  const props = defineProps<Props>()
  
  const formatAmount = (amount: number): string => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP',
      minimumFractionDigits: 2
    }).format(amount)
  }
  
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
  
  const chartOptions = {
    plugins: {
      legend: {
        display: false,        
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const value = context.raw as number
            return `${context.label}: ${formatAmount(value)}`
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