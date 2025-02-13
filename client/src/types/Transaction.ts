export interface Transaction {
  id: string
  date: string
  amount: number
  description: string
  notes: string | null
  category_id: string
  merchant_id: string | null
}
export interface Category {
  id: string
  title: string
  color: string
}

export interface AnalyticsResponse {
  categories: Array<{
    id: string | null
    total: string
  }>
  total: string
}
export interface TransactionState {
  showAllTransactions: boolean
  currentMonth: string
  isLoading: boolean
  error: string | null
}
