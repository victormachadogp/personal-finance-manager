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
    <div v-else-if="store.analyticsSummary" class="bg-white flex flex-col px-7 pb-8 pt-4 gap-2 rounded-[0.3rem]">      
      <div class="flex justify-end mb-4">
        <button 
          @click="toggleChart" 
          class="hover:opacity-70 transition-opacity"
        >
        <ChartIcon class="w-5 h-5" />
      </button>

      </div>
      <AnalyticsItem
        v-for="item in store.analyticsSummary.items"
        :key="item.categoryId || 'uncategorized'"
        :item="item"
      />

      <div class="flex justify-between text-xs font-medium border-t mt-4 pt-3">
        <span>Total</span>
        <span>{{ currencySymbol }}{{ store.analyticsSummary.total }}</span>
      </div>
      <AnalyticsChart 
        v-if="isChartVisible"
        :summary="store.analyticsSummary" 
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTransactionStore } from '../stores/transactionStore'
import { useAccountStore } from '../stores/accountStore'
import AnalyticsItem from './AnalyticsItem.vue'
import AnalyticsChart from './AnalyticsChart.vue'
import ChartIcon from './icons/ChartIcon.vue'

const store = useTransactionStore()
const accountStore = useAccountStore()
const isChartVisible = ref(false)

const toggleChart = () => {
  isChartVisible.value = !isChartVisible.value
}

const currencySymbol = accountStore.selectedCurrency?.symbol || ''


onMounted(async () => {
  await store.fetchCategories()
})
</script>