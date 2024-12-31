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
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ArrowLeft from './icons/ArrowLeft.vue'
import ArrowRight from './icons/ArrowRight.vue'

const route = useRoute()
const router = useRouter()

const currentMonth = ref(new Date())

const monthParam = route.query.month as string | undefined
if (monthParam) {
  currentMonth.value = new Date(monthParam + '-01')
}

const formattedMonth = computed(() => {
  return currentMonth.value.toLocaleString('default', { month: 'long', year: 'numeric' })
})

const navigate = (direction: number) => {
  currentMonth.value.setMonth(currentMonth.value.getMonth() + direction)
  const newMonth = currentMonth.value.toISOString().slice(0, 7)
  router.push({ query: { ...route.query, month: newMonth } })
}

// Watch for changes in the route query parameter and update currentMonth accordingly
watch(
  () => route.query.month,
  (newMonth) => {
    if (newMonth) {
      currentMonth.value = new Date(newMonth + '-01')
    }
  }
)
</script>

<style scoped></style>
