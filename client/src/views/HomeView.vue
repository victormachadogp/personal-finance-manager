<template>
  <main class="w-4/5 mx-auto grid grid-cols-2 pt-5">
    <div class="flex flex-col justify-between grid-span-1">
        <PeriodNavigator class="mb-10" />
        <TransactionList />
      </div>
      <div class="grid-span-1">
        <AnalyticsSummary />
      </div>

  </main>
</template>

<script setup lang="ts">
import AnalyticsSummary from '../components/AnalyticsSummary.vue';
import PeriodNavigator from '../components/PeriodNavigator.vue';
import TransactionList from '../components/TransactionList.vue';
</script>
