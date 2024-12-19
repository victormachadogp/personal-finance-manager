<template>
    <div class="w-[420px] mt-[55px]">
      <h2 class="font-medium mb-4">Analytics</h2>
      
      <div class="bg-white flex flex-col px-7 py-8 gap-2 rounded-[0.3rem]">        

        <AnalyticsItem 
        v-for="item in analyticsData"
        :key="item.category"
        :item="item"
        />
        
        <div class="flex justify-between text-xs font-medium border-t mt-4 pt-3">
           <span>Total</span>
           <span>-464.53</span> 
        </div>
      </div>
    </div>
  </template>

  <script setup lang="ts">
  import { ref } from 'vue'
  import AnalyticsItem from './AnalyticsItem.vue'

  const analyticsData = ref([
  {
    category: 'Meal Service',
    amount: 406.29,
    color: '#22c55e'
  },
  {
    category: 'Shopping',
    amount: 96.29,
    color: '#a855f7'
  },
  {
    category: 'General',
    amount: 204.53,
    color: '#3b82f6'
  }
])
  
  </script>