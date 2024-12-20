<template>
    <div class="w-[80%]">
      <div v-if="isLoading" class="loading">Loading...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      
      <template v-else>
        
        
        <div v-for="(transactions, date) in groupedTransactions" :key="date">
          <TransactionDateGroup 
            :date="date"
            :transactions="transactions"
          />
        </div>
      </template>
    </div>
  </template>
  
<script setup lang="ts">
import { onMounted } from 'vue'
import TransactionDateGroup from './TransactionDateGroup.vue'
import { useTransactions } from '../services/transactionService';

const {
  isLoading,
  error,
  groupedTransactions,
  fetchTransactions,
  fetchCategories
} = useTransactions()

onMounted(async () => {
  await Promise.all([fetchTransactions(), fetchCategories()])
})
</script>
