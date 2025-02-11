import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { TransactionService } from '../services/transactionService'
import { UrlService } from '../services/urlService'
import { useTransactionStore } from '../stores/transactionStore'

export function useTransactionManager() {
  const router = useRouter()
  const route = useRoute()
  const store = useTransactionStore()
  const transactionService = new TransactionService()
  const urlService = new UrlService(router, route)

  const currentMonth = ref(new Date().toISOString().slice(0, 7))

  const initialize = async () => {
    const { month, showAll } = urlService.getInitialState()

    if (month) {
      currentMonth.value = month
    }

    store.setShowAllTransactions(showAll)

    await Promise.all([
      store.fetchCategories(transactionService),
      store.refreshData(transactionService, currentMonth.value),
    ])

    urlService.updateURL(store.showAllTransactions, currentMonth.value)
  }

  const handleMonthChange = async (month: string) => {
    currentMonth.value = month
    await store.refreshData(transactionService, month)
    urlService.updateURL(store.showAllTransactions, month)
  }

  const handleViewModeChange = async () => {
    store.setShowAllTransactions(!store.showAllTransactions)
    await store.refreshData(transactionService, currentMonth.value)
    urlService.updateURL(store.showAllTransactions, currentMonth.value)
  }

  const handleUrlChange = async (query: Record<string, string>) => {
    const newMonth = query.month
    const showAll = query.showAll === 'true'

    if (showAll !== store.showAllTransactions) {
      store.setShowAllTransactions(showAll)
    }

    if (newMonth && newMonth !== currentMonth.value) {
      currentMonth.value = newMonth
    }

    await store.refreshData(transactionService, newMonth)
  }

  return {
    currentMonth,
    initialize,
    handleMonthChange,
    handleViewModeChange,
    handleUrlChange,
  }
}
