import type { TransactionServiceInterface } from '../types/TransactionServiceInterface'

export class LiveTransactionService implements TransactionServiceInterface {
  private readonly BASE_URL = import.meta.env.VITE_API_URL

  async fetchTransactions(month?: string, showAll?: boolean): Promise<Transaction[]> {
    const params = new URLSearchParams()
    if (month && !showAll) params.append('month', month)
    if (showAll) params.append('all', 'true')

    const response = await fetch(`${this.BASE_URL}/transactions?${params.toString()}`)
    return response.json()
  }

  async fetchCategories(): Promise<Category[]> {
    const response = await fetch(`${this.BASE_URL}/categories`)
    return response.json()
  }

  async fetchAnalytics(month?: string, showAll: boolean = false): Promise<AnalyticsResponse> {
    const url = new URL(`${this.BASE_URL}/categories/analytics`)
    if (month && !showAll) {
      url.searchParams.append('month', month)
    }
    const response = await fetch(url)
    return await response.json()
  }
}
