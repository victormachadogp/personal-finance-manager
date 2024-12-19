import { ref, computed } from 'vue'
import type { Transaction, Category } from '../types/Transaction'

const BASE_URL = 'http://localhost:3000'

export function useTransactions() {
  const transactions = ref<Transaction[]>([])
  const categories = ref<Category[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchTransactions = async () => {
    isLoading.value = true
    try {
      const response = await fetch(`${BASE_URL}/transactions`)
      transactions.value = await response.json()
    } catch (e) {
      error.value = 'Failed to fetch transactions'
    } finally {
      isLoading.value = false
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${BASE_URL}/categories`)
      categories.value = await response.json()
    } catch (e) {
      error.value = 'Failed to fetch categories'
    }
  }

  const groupedTransactions = computed(() => {
    const groups: Record<string, Transaction[]> = {}
    transactions.value.forEach((transaction) => {
      const date = transaction.date
      if (!groups[date]) {
        groups[date] = []
      }
      groups[date].push(transaction)
    })
    return groups
  })

  return {
    transactions,
    categories,
    isLoading,
    error,
    fetchTransactions,
    fetchCategories,
    groupedTransactions,
  }
}
