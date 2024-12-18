export interface Transaction {
  id: string
  date: string
  amount: number
  description: string
  notes: string | null
  category_id: string
  merchant_id: string | null
}
