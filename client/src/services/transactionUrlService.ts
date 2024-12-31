import { ref } from 'vue'
import type { Router, RouteLocationNormalizedLoaded } from 'vue-router'
import { useTransactionStore } from '../stores/transactionStore'

export class TransactionUrlService {
  private currentMonth = ref(new Date().toISOString().slice(0, 7))
  private store
  private router: Router
  private route: RouteLocationNormalizedLoaded

  constructor(router: Router, route: RouteLocationNormalizedLoaded) {
    this.store = useTransactionStore()
    this.router = router
    this.route = route
    this.initializeFromUrl()
  }

  private initializeFromUrl() {
    const monthFromUrl = this.route.query.month as string
    if (monthFromUrl) {
      this.currentMonth.value = monthFromUrl
    }

    const showAllFromUrl = this.route.query.showAll === 'true'
    this.store.showAllTransactions = showAllFromUrl
  }

  private updateURL() {
    this.router.replace({
      query: {
        ...(this.store.showAllTransactions ? { showAll: 'true' } : {}),
        ...(!this.store.showAllTransactions ? { month: this.currentMonth.value } : {}),
      },
    })
  }

  async handleMonthChange(month: string) {
    this.currentMonth.value = month
    await this.store.refreshData(month)
    this.updateURL()
  }

  async handleViewModeChange() {
    await this.store.toggleViewMode(this.currentMonth.value)
    this.updateURL()
  }

  async handleUrlChange(query: Record<string, string>) {
    const newMonth = query.month
    const showAll = query.showAll === 'true'

    if (showAll !== this.store.showAllTransactions) {
      this.store.showAllTransactions = showAll
    }

    if (newMonth && newMonth !== this.currentMonth.value) {
      this.currentMonth.value = newMonth
    }

    await this.store.refreshData(newMonth)
  }

  async initialize() {
    await Promise.all([
      this.store.fetchCategories(),
      this.store.refreshData(this.currentMonth.value),
    ])
    this.updateURL()
  }

  getCurrentMonth() {
    return this.currentMonth
  }
}
