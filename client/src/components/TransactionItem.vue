<template>
  <div class="transaction">
    <div class="flex items-center relative">
      <div class="flex items-center gap-2 flex-1 whitespace-nowrap max-w-[50%]">
        <h4 
          ref="descriptionEl"
          class="text-sm font-medium text-ellipsis overflow-hidden relative"
          @mouseenter="showTooltip"
          @mouseleave="hideTooltip"
        >
          {{ transaction.description }}
        </h4>
        <span v-if="transaction.notes" class="text-xs text-[#8E8E93]">
          {{ transaction.notes }}
        </span>
      </div>
      
      <div v-if="category" class="flex mx-2 items-center ml-5">
        <div 
          class="w-2 h-2 rounded-full mr-2" 
          :style="{ backgroundColor: category.color }"
        ></div>
        <span class="text-xs">
          {{ category.title }}
        </span>
      </div>
      
      <div class="ml-auto text-xs font-medium">
        {{ formatAmount(transaction.amount) }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, inject } from 'vue'
import type { Transaction, Category } from '../types/Transaction'

const props = defineProps<{
  transaction: Transaction
  category?: Category
}>()

const descriptionEl = ref<HTMLElement | null>(null)
const showGlobalTooltip = inject('showGlobalTooltip') as (text: string, element: HTMLElement) => void
const hideGlobalTooltip = inject('hideGlobalTooltip') as () => void

const checkIfTruncated = (): boolean => {
  if (descriptionEl.value) {
    return descriptionEl.value.offsetWidth < descriptionEl.value.scrollWidth
  }
  return false
}

const showTooltip = () => {
  if (checkIfTruncated() && descriptionEl.value) {
    showGlobalTooltip(props.transaction.description, descriptionEl.value)
  }
}

const hideTooltip = () => {
  hideGlobalTooltip()
}

onMounted(() => {
  window.addEventListener('resize', checkIfTruncated)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkIfTruncated)
})

const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(amount)
}
</script>