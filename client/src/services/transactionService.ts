import { ref, computed } from 'vue'
import type { Transaction, Category } from '../types/Transaction'
import type { AnalyticsResponse, AnalyticsSummary, AnalyticsItem } from '../types/Analytics'

const BASE_URL = import.meta.env.VITE_API_URL

export function useTransactions() {
  const transactions = ref<Transaction[]>([])
  const categoryMap = ref<Map<string, Category>>(new Map())
  const analyticsData = ref<AnalyticsResponse | null>(null)
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
      const categoriesList = await response.json()
      categoryMap.value = new Map(categoriesList.map((category) => [category.id, category]))
    } catch (e) {
      error.value = 'Failed to fetch categories'
    }
  }
  const getCategory = (categoryId: string | null) => {
    if (!categoryId) return undefined
    return categoryMap.value.get(categoryId)
  }

  const groupedTransactions = computed(() => {
    const groups: Record<string, (Transaction & { category?: Category })[]> = {}

    transactions.value.forEach((transaction) => {
      const date = transaction.date
      if (!groups[date]) {
        groups[date] = []
      }
      // Já incluímos a categoria junto com a transação
      const transactionWithCategory = {
        ...transaction,
        category: getCategory(transaction.category_id),
      }
      groups[date].push(transactionWithCategory)
    })
    return groups
  })

  const fetchAnalytics = async () => {
    try {
      const response = await fetch(`${BASE_URL}/categories/analytics`)
      analyticsData.value = await response.json()
    } catch (e) {
      error.value = 'Failed to fetch analytics'
    }
  }

  const analyticsSummary = computed((): AnalyticsSummary | null => {
    if (!analyticsData.value) return null

    const total = parseFloat(analyticsData.value.total)

    const items: AnalyticsItem[] = analyticsData.value.categories
      .map((categoryAnalytics) => {
        const category = categoryAnalytics.id
          ? categoryMap.value.get(categoryAnalytics.id)
          : { title: 'Uncategorized', color: '#94A3B8' } // Default for null category

        const categoryTotal = parseFloat(categoryAnalytics.total)

        return {
          categoryId: categoryAnalytics.id,
          category: category?.title || 'Unknown',
          total: categoryTotal,
          color: category?.color || '#94A3B8',
          percentage: (categoryTotal / total) * 100,
        }
      })
      .sort((a, b) => b.total - a.total)

    return {
      items,
      total,
    }
  })

  return {
    isLoading,
    error,
    fetchTransactions,
    fetchCategories,
    fetchAnalytics,
    groupedTransactions,
    analyticsSummary,
  }
}
