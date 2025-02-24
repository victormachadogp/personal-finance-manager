import { defineStore } from 'pinia'
import { TransactionService } from '../services/transactionService'
import type { Transaction, Category } from '../types/Transaction'
import type { AnalyticsResponse, AnalyticsSummary, AnalyticsItem } from '../types/Analytics'

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
    async fetchTransactions(transactionService: TransactionService, month?: string) {
      this.isLoading = true
      try {
        this.transactions = await transactionService.fetchTransactions(
          month,
          this.showAllTransactions,
        )
        if (month && !this.showAllTransactions) {
          this.selectedMonth = month
        }
        this.error = null
      } catch (e) {
        this.error = 'Failed to fetch transactions'
      } finally {
        this.isLoading = false
      }
    },

    async fetchCategories(transactionService: TransactionService) {
      try {
        const categoriesList = await transactionService.fetchCategories()
        this.categoryMap = new Map(categoriesList.map((category) => [category.id, category]))
        this.error = null
      } catch (e) {
        this.error = 'Failed to fetch categories'
      }
    },

    async fetchAnalytics(transactionService: TransactionService, month?: string) {
      try {
        this.analyticsData = await transactionService.fetchAnalytics(
          month,
          this.showAllTransactions,
        )
        this.error = null
      } catch (e) {
        this.error = 'Failed to fetch analytics'
      }
    },

    setShowAllTransactions(value: boolean) {
      this.showAllTransactions = value
    },

    async refreshData(transactionService: TransactionService, month?: string) {
      await Promise.all([
        this.fetchTransactions(transactionService, month),
        this.fetchAnalytics(transactionService, month),
      ])
    },
  },
})
