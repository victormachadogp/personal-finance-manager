import { defineStore } from 'pinia'
import type { Transaction, Category } from '../types/Transaction'
import type { AnalyticsResponse, AnalyticsSummary, AnalyticsItem } from '../types/Analytics'

const BASE_URL = import.meta.env.VITE_API_URL

export const useTransactionStore = defineStore('transaction', {
  state: () => ({
    transactions: [] as Transaction[],
    categoryMap: new Map() as Map<string, Category>,
    analyticsData: null as AnalyticsResponse | null,
    isLoading: false,
    error: null as string | null,
    selectedMonth: null as string | null,
    showAllTransactions: false,
  }),

  getters: {
    groupedTransactions: (state) => {
      const groups: Record<string, (Transaction & { category?: Category })[]> = {}

      state.transactions.forEach((transaction) => {
        const date = transaction.date
        if (!groups[date]) {
          groups[date] = []
        }
        const category = state.categoryMap.get(transaction.category_id ?? '')
        groups[date].push({ ...transaction, category })
      })
      return groups
    },

    analyticsSummary: (state): AnalyticsSummary | null => {
      if (!state.analyticsData) return null

      const total = parseFloat(state.analyticsData.total)

      const items: AnalyticsItem[] = state.analyticsData.categories
        .map((categoryAnalytics) => {
          const category = categoryAnalytics.id
            ? state.categoryMap.get(categoryAnalytics.id)
            : { title: 'Uncategorized', color: '#94A3B8' }

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
    },
  },

  actions: {
    async fetchTransactions(month?: string) {
      this.isLoading = true
      try {
        const url = new URL(`${BASE_URL}/transactions`)
        if (month && !this.showAllTransactions) {
          url.searchParams.append('month', month)
          this.selectedMonth = month
        }
        const response = await fetch(url)
        this.transactions = await response.json()
        this.error = null
      } catch (e) {
        this.error = 'Failed to fetch transactions'
      } finally {
        this.isLoading = false
      }
    },

    async fetchCategories() {
      try {
        const response = await fetch(`${BASE_URL}/categories`)
        const categoriesList = await response.json()
        this.categoryMap = new Map(categoriesList.map((category) => [category.id, category]))
        this.error = null
      } catch (e) {
        this.error = 'Failed to fetch categories'
      }
    },

    async fetchAnalytics(month?: string) {
      try {
        const url = new URL(`${BASE_URL}/categories/analytics`)
        if (month && !this.showAllTransactions) {
          url.searchParams.append('month', month)
        }
        const response = await fetch(url)
        this.analyticsData = await response.json()
        this.error = null
      } catch (e) {
        this.error = 'Failed to fetch analytics'
      }
    },

    async toggleViewMode(month?: string) {
      this.showAllTransactions = !this.showAllTransactions
      await Promise.all([this.fetchTransactions(month), this.fetchAnalytics(month)])
    },

    async refreshData(month?: string) {
      await Promise.all([this.fetchTransactions(month), this.fetchAnalytics(month)])
    },
  },
})
