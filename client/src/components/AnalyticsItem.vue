<template>
  <div class="flex items-center justify-between relative">
    <div class="flex items-center gap-2">
      <div 
        class="w-3 h-3 rounded-full"
        :style="{ backgroundColor: item.color }"
      ></div>
      <span class="text-xs whitespace-nowrap">{{ item.category }}</span>
    </div>
    <div class="w-[150px] h-1.5 bg-[#F3F1F1] rounded-full absolute left-[35%]">
      <div
        :style="{ 
          backgroundColor: item.color,
          width: `${item.percentage}%`
        }"
        class="h-full rounded-full"
      ></div>
    </div>
    <div>
      <span class="text-xs flex">{{ currencySymbol }}{{ item.total }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { AnalyticsItem } from '../types/Analytics'
import { useAccountStore } from '../stores/accountStore'

const accountStore = useAccountStore()

const currencySymbol = accountStore.selectedCurrency?.symbol || ''

const props = defineProps<{
  item: AnalyticsItem
}>()
</script>