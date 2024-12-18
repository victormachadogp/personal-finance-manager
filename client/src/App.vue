<template>
  <header>

      <nav class="flex justify-center gap-5">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    
    {{transactions}}
  </header>


  <RouterView />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { transactionService } from './services/transactionService'
import type { Transaction } from './types/Transaction'

const transactions = ref<Transaction[]>([])

const fetchTransactions = async () => {
  try {
    transactions.value = await transactionService.fetchTransactions()
  } catch (error) {
    console.error('Error loading transactions:', error)
  }
}

onMounted(() => {
  fetchTransactions()
})
</script>
