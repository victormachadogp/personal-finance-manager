<template>
    <div class="transaction">
      <div class="flex items-center relative">
        <div class="flex items-center gap-2 flex-1">
          <h4 class="text-sm font-medium">{{ transaction.description }}</h4>
          <span v-if="transaction.notes" class="text-xs text-[#8E8E93]">
            {{ transaction.notes }}
          </span>
        </div>
        <div
          v-if="category" 
          class="flex mx-2 grow items-center justify-end absolute left-[50%] translate-x-[0%]">
        
        <div
         class="w-2 h-2 rounded-full mr-2"
         :style="{ backgroundColor: `${category.color}20` }"
         ></div>
          <span 
            class="text-xs"            
          >
            {{ category.name }}
          </span>
        </div>
        <div class="ml-auto text-xs font-medium">
          {{ formatAmount(transaction.amount) }}
        </div>
      </div>
    </div>
  </template>

<script setup lang="ts">
import type { Transaction, Category } from '../types/Transaction'

const props = defineProps<{
  transaction: Transaction
  category?: Category
}>()

const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(amount)
}
</script>