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
          <Teleport to="body">
            <div 
              v-if="isTooltipVisible && isTextTruncated" 
              class="fixed z-50 bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-normal max-w-xs"
              :style="tooltipStyle"
            >
              {{ transaction.description }}
            </div>
          </Teleport>
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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import type { Transaction, Category } from '../types/Transaction'

const props = defineProps<{
  transaction: Transaction
  category?: Category
}>()

const descriptionEl = ref<HTMLElement | null>(null)
const isTooltipVisible = ref(false)
const isTextTruncated = ref(false)
const tooltipPosition = ref({ x: 0, y: 0 })

const tooltipStyle = computed(() => ({
  left: `${tooltipPosition.value.x}px`,
  top: `${tooltipPosition.value.y}px`
}))

const checkIfTruncated = () => {
  if (descriptionEl.value) {
    isTextTruncated.value = descriptionEl.value.offsetWidth < descriptionEl.value.scrollWidth
  }
}

const updateTooltipPosition = () => {
  if (descriptionEl.value) {
    const rect = descriptionEl.value.getBoundingClientRect()
    tooltipPosition.value = {
      x: rect.left,
      y: rect.top - 30 // position 30px above the element
    }
  }
}

const showTooltip = () => {
  if (isTextTruncated.value) {
    updateTooltipPosition()
    isTooltipVisible.value = true
  }
}

const hideTooltip = () => {
  isTooltipVisible.value = false
}

onMounted(() => {
  checkIfTruncated()
  window.addEventListener('resize', checkIfTruncated)
  window.addEventListener('scroll', updateTooltipPosition, true)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkIfTruncated)
  window.removeEventListener('scroll', updateTooltipPosition, true)
})

const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(amount)
}
</script>