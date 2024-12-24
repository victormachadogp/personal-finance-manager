<template>
  <div class="w-[420px] mt-[55px]">
    <div class="flex items-center justify-between">
    <h2 class="font-medium mb-4">Analytics</h2>
      <div class="mb-4 text-sm text-gray-600">
        <span v-if="store.showAllTransactions">All Transactions</span>
        <span v-else>{{ store.selectedMonth }}</span>
      </div>
  </div>
    <div v-if="store.isLoading" class="loading">Loading...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>
    <div v-else-if="store.analyticsSummary" class="bg-white flex flex-col px-7 py-8 gap-2 rounded-[0.3rem]">
      <AnalyticsItem
        v-for="item in store.analyticsSummary.items"
        :key="item.categoryId || 'uncategorized'"
        :item="item"
      />

      <div class="flex justify-between text-xs font-medium border-t mt-4 pt-3">
        <span>Total</span>
        <span>{{ formatAmount(store.analyticsSummary.total) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useTransactionStore } from '../stores/transactionStore'
import AnalyticsItem from './AnalyticsItem.vue'

const store = useTransactionStore()

const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
    minimumFractionDigits: 2
  }).format(amount)
}

onMounted(async () => {
  await store.fetchCategories()
})
</script>