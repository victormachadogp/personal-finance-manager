<template>
    <div class="flex items-center justify-between relative">
        <div class="flex items-center gap-2">
            <div class="w-3 h-3 bg-gray-500 rounded-full"></div>
            <span class="text-xs whitespace-nowrap	">{{ item.category }}</span>
        </div>
        <div class="w-[150px] h-1.5 bg-[#F3F1F1] rounded-full absolute left-[35%]">
            <div
            :style="{ backgroundColor: item.color }"
            class="h-full w-1/2 rounded-full "></div>
        </div>
        <div>
            <span class="text-xs flex">-{{ formatAmount(item.amount) }}</span>
        </div>
    </div>
  </template>

<script setup lang="ts">
const props = defineProps<{
  item: AnalyticsItem
  total: number
}>()

const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
    minimumFractionDigits: 2
  }).format(amount)
}

defineOptions({
  name: 'AnalyticsItem'
})
</script>
