<template>
  <div class="flex gap-6 self-start">
    <button @click="navigate(-1)">
      <ArrowLeft />
    </button>
    <h2 class="font-medium">{{ formattedMonth }}</h2>
    <button @click="navigate(1)">
      <ArrowRight />
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ArrowLeft from './icons/ArrowLeft.vue'
import ArrowRight from './icons/ArrowRight.vue'
import { TransactionUrlService } from '../services/transactionUrlService'

const route = useRoute()
const router = useRouter()

const urlService = new TransactionUrlService(router, route)
const currentMonth = urlService.getCurrentMonth()

const formattedMonth = computed(() => {
  const [year, month] = currentMonth.value.split('-')
  return new Date(Number(year), Number(month) - 1).toLocaleString('default', { month: 'long', year: 'numeric' })
})

const navigate = (direction: number) => {
  const [year, month] = currentMonth.value.split('-').map(Number)
  const newDate = new Date(year, month - 1 + direction)
  currentMonth.value = newDate.toISOString().slice(0, 7)
  router.push({ query: { ...route.query, month: currentMonth.value } })
}

// Watch for changes in the route query parameter and update currentMonth accordingly
watch(() => route.query.month, (newMonth) => {
  if (newMonth) currentMonth.value = newMonth as string
})
</script>

<style scoped></style>
