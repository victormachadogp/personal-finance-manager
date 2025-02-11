<template>
  <div class="w-[80%]">
    <div class="mb-6 flex items-center gap-4">
      <div class="flex items-center gap-2">
        <input type="checkbox" :checked="store.showAllTransactions" @change="handleViewModeChange" id="viewMode"
          class="form-checkbox h-4 w-4" />
        <label for="viewMode" class="text-sm text-gray-700">Show all transactions</label>
      </div>

      <input v-if="!store.showAllTransactions" type="month" v-model="currentMonth" @change="handleMonthChange"
        class="px-4 py-2 border rounded-md" />
    </div>

    <div v-if="store.isLoading" class="loading">Loading...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>

    <template v-else>
      <div v-for="(transactions, date) in store.groupedTransactions" :key="date">
        <TransactionDateGroup :date="date" :transactions="transactions" />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import TransactionDateGroup from './TransactionDateGroup.vue'
import { useTransactionStore } from '../stores/transactionStore'
import { useTransactionManager } from '../composables/useTransactionManager'

const store = useTransactionStore()
const route = useRoute()
const {
  currentMonth,
  initialize,
  handleMonthChange,
  handleViewModeChange,
  handleUrlChange
} = useTransactionManager()

watch(() => route.query, (newQuery) => handleUrlChange(newQuery as Record<string, string>))

onMounted(() => initialize())
</script>
