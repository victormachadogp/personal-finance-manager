export class TransactionService {
  private baseUrl: string

  constructor() {
    this.baseUrl = import.meta.env.VITE_API_URL
  }

  async fetchTransactions(month?: string, showAll: boolean = false) {
    const url = new URL(`${this.baseUrl}/transactions`)
    if (month && !showAll) {
      url.searchParams.append('month', month)
    }
    const response = await fetch(url)
    return await response.json()
  }

  async fetchCategories() {
    const response = await fetch(`${this.baseUrl}/categories`)
    return await response.json()
  }

  async fetchAnalytics(month?: string, showAll: boolean = false) {
    const url = new URL(`${this.baseUrl}/categories/analytics`)
    if (month && !showAll) {
      url.searchParams.append('month', month)
    }
    const response = await fetch(url)
    return await response.json()
  }
}
