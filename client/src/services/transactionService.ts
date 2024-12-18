import type { Transaction } from '@/types/Transaction'

const BASE_URL = 'http://localhost:3001'

export const transactionService = {
  async fetchTransactions(): Promise<Transaction[]> {
    try {
      const response = await fetch(`${BASE_URL}/transactions`)

      if (!response.ok) {
        throw new Error(`Error HTTP! status: ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('Error retrieving transactions:', error)
      throw error
    }
  },
}
