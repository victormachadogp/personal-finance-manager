import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const BASE_URL = import.meta.env.VITE_API_URL

interface Currency {
  id: string
  name: string
  symbol: string
  bcp_47_lang_tag: string
}

interface Account {
  id: string
  name: string
  currency: Currency
}

export const useAccountStore = defineStore('account', () => {
  const accounts = ref<Account[]>([])
  const selectedCurrency = ref<Currency | null>(null)

  const getCurrencyCode = (currencyId: string): string => {
    return currencyId.toUpperCase()
  }

  const formatter = computed(() => {
    if (!selectedCurrency.value) {
      return new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: 'GBP',
      })
    }

    return new Intl.NumberFormat(selectedCurrency.value.bcp_47_lang_tag, {
      style: 'currency',
      currency: getCurrencyCode(selectedCurrency.value.id),
    })
  })

  const formatCurrency = (amount: number) => {
    return formatter.value.format(amount)
  }

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
    accounts,
    selectedCurrency,
    fetchAccounts,
    formatCurrency,
  }
})
