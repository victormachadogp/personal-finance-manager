<template>
  <div class="w-[420px] mt-[55px]">
    <h2 class="font-medium mb-4">Analytics</h2>

    <div v-if="isLoading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="analyticsSummary" class="bg-white flex flex-col px-7 py-8 gap-2 rounded-[0.3rem]">
      <AnalyticsItem
        v-for="item in analyticsSummary.items"
        :key="item.categoryId || 'uncategorized'"
        :item="item"
      />

      <div class="flex justify-between text-xs font-medium border-t mt-4 pt-3">
        <span>Total</span>
        <span>{{ formatAmount(analyticsSummary.total) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useTransactions } from '../services/transactionService'
import AnalyticsItem from './AnalyticsItem.vue'

const { 
  analyticsSummary, 
  isLoading, 
  error, 
  fetchCategories, 
  fetchAnalytics 
} = useTransactions()

const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
    minimumFractionDigits: 2
  }).format(amount)
}

onMounted(async () => {
  await Promise.all([fetchCategories(), fetchAnalytics()])
})
</script>