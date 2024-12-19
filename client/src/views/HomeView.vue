<template>
  <main class="flex flex-col pt-5 bg-[#EBEDF0]">
    
    <PeriodNavigator class="mb-10" />
      
      <div class="flex justify-between">

        <TransactionList />
      </div>

  </main>
</template>

<script setup lang="ts">
import PeriodNavigator from '../components/PeriodNavigator.vue';
import TransactionList from '../components/TransactionList.vue';
</script>