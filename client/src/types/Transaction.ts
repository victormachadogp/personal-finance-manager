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
export interface TransactionState {
  showAllTransactions: boolean
  currentMonth: string
  isLoading: boolean
  error: string | null
}
