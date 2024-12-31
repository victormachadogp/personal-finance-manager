import { defineStore } from 'pinia'
import { ref } from 'vue'

const BASE_URL = import.meta.env.VITE_API_URL

interface Currency {
  id: string
  name: string
  code: string
  symbol: string
}

interface Account {
  id: string
  name: string
  currency: Currency
}

export const useAccountStore = defineStore('account', () => {
  const accounts = ref<Account[]>([])
  const selectedCurrency = ref<Currency | null>(null)

  const fetchAccounts = async () => {
    try {
      const response = await fetch(`${BASE_URL}/accounts`)
      accounts.value = await response.json()
      if (accounts.value.length > 0) {
        selectedCurrency.value = accounts.value[0].currency
      }
    } catch (error) {
      console.error('Failed to fetch accounts:', error)
    }
  }

  return {
    selectedCurrency,
    fetchAccounts,
  }
})
