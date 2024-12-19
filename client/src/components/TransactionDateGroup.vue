<template>
    <div class="mb-7">
      <h3 class="text-[#5e5f60] text-sm font-medium mb-3">{{ formattedDate }}</h3>
      <div class=" flex flex-col bg-white rounded-[0.3rem] p-5 gap-4">
        <TransactionItem
          v-for="transaction in transactions"
          :key="transaction.id"
          :transaction="transaction"
          :category="findCategory(transaction.category_id)"
        />
      </div>
    </div>
  </template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Transaction, Category } from '../types/Transaction'
import TransactionItem from '../components/TransactionItem.vue';

const props = defineProps<{
  date: string
  transactions: Transaction[]
  categories: Category[]
}>()

const formattedDate = computed(() => {
  return new Date(props.date).toLocaleDateString('en-US', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    timeZone: 'UTC',
  })
})

const findCategory = (categoryId: string): Category | undefined => {
  return props.categories.find(category => category.id === categoryId)
}
</script>