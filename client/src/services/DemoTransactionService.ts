import { TransactionServiceInterface } from '../types/TransactionServiceInterface'
import type { Transaction, Category, AnalyticsResponse } from '../types/Transaction'

export class DemoTransactionService implements TransactionServiceInterface {
  private readonly demoCategories: Category[] = [
    {
      icon: 'rectangle-stack',
      title: 'General',
      id: 'k2Bnio4r4rumjEtf7KAnRP',
      color: '#808080',
    },
    {
      icon: 'truck',
      title: 'Transport',
      id: 'nmvY3NerXM3t8n3GCD3S9e',
      color: '#4B77BE',
    },
    {
      icon: 'home',
      title: 'Housing',
      id: '8dbxskvYv3k672TJCjniQx',
      color: '#8B4513',
    },
    {
      icon: 'shopping-cart',
      title: 'Groceries',
      id: 'anXz4uDvzF29jzUqX7cyPq',
      color: '#FF9800',
    },
    {
      icon: 'shopping-bag',
      title: 'Shopping',
      id: '3v2znBBbuK6aDTAkRdfsB6',
      color: '#FF69B4',
    },
    {
      icon: 'credit-card',
      title: 'Bills',
      id: 'TETAxd9u4he5dCWXZbBpRh',
      color: '#D32F2F',
    },
    {
      icon: 'film',
      title: 'Entertainment',
      id: 'TZuwyBFHemk95U6avZfvEf',
      color: '#9B59B6',
    },
    {
      icon: 'cake',
      title: 'Eating Out',
      id: 'TdTY9ahjNKanyAvyUCmUth',
      color: '#F1C40F',
    },
    {
      icon: 'gift',
      title: 'Charity',
      id: 'AXLpno5SHNDB2WXvQSdzCZ',
      color: '#87CEEB',
    },
    {
      icon: 'heart',
      title: 'Personal Care',
      id: 'nK9LfGwKsFpv87XY8FYLY2',
      color: '#1ABC9C',
    },
    {
      icon: 'briefcase',
      title: 'Business',
      id: '8GshVk2jfcs4BKnLTVzx2w',
      color: '#34495E',
    },
    {
      icon: 'academic-cap',
      title: 'Education',
      id: 'Q3enGA7mRz3zGE59edkhBB',
      color: '#3498DB',
    },
    {
      icon: 'chart-bar',
      title: 'Investments',
      id: 'YdkFskyaobeDR4dVmFqUv9',
      color: '#27AE60',
    },
    {
      icon: 'calendar',
      title: 'Holidays',
      id: 'Liwwdaqt7fPJ6LKFACjpiX',
      color: '#00BCD4',
    },
    {
      icon: 'currency-pound',
      title: 'Cash',
      id: 'RDrzJ8BzASa6yNgecSPSfF',
      color: '#16A085',
    },
    {
      icon: 'currency-dollar',
      title: 'Income',
      id: 'jHC68t25b7qtqkUQq4Ny3C',
      color: '#16A085',
    },
  ]

  private readonly demoTransactions: Transaction[] = [
    {
      date: '2024-12-16T00:00:00',
      description: 'TESCO EXPRESS OXFORD ST LONDON',
      notes: null,
      merchant_id: null,
      exclude_from_analytics: false,
      id: 'MzeQTsFVgDLigSZseYD3kE',
      amount: '55.73',
      category_id: 'anXz4uDvzF29jzUqX7cyPq',
      account_id: 'amex',
    },
    {
      date: '2024-12-16T00:00:00',
      description: 'SAINSBURY LOCAL BRISTOL',
      notes: null,
      merchant_id: null,
      exclude_from_analytics: false,
      id: 'NkACEGSFrNcYQXcHWBxcTS',
      amount: '34.04',
      category_id: 'anXz4uDvzF29jzUqX7cyPq',
      account_id: 'amex',
    },
    {
      date: '2024-12-16T00:00:00',
      description: 'HOLIDAY INN LONDON',
      notes: null,
      merchant_id: null,
      exclude_from_analytics: false,
      id: 'd5pcA4xvqNjsjtS8PH5rE8',
      amount: '2924.53',
      category_id: 'Liwwdaqt7fPJ6LKFACjpiX',
      account_id: 'amex',
    },
    {
      date: '2024-12-16T00:00:00',
      description: 'H&M OXFORD ST',
      notes: null,
      merchant_id: null,
      exclude_from_analytics: false,
      id: 'KjpcB5xvqNjsjtS8PH5rE9',
      amount: '1234.64',
      category_id: '3v2znBBbuK6aDTAkRdfsB6',
      account_id: 'amex',
    },
    {
      date: '2024-12-16T00:00:00',
      description: 'UBER TRIP LONDON',
      notes: null,
      merchant_id: null,
      exclude_from_analytics: false,
      id: 'LmpcC6xvqNjsjtS8PH5rF0',
      amount: '596.45',
      category_id: 'nmvY3NerXM3t8n3GCD3S9e',
      account_id: 'amex',
    },
    {
      date: '2024-12-14T00:00:00',
      description: 'VUE CINEMA BRISTOL',
      notes: null,
      merchant_id: null,
      exclude_from_analytics: false,
      id: 'PqpcD7xvqNjsjtS8PH5rF1',
      amount: '518.25',
      category_id: 'TZuwyBFHemk95U6avZfvEf',
      account_id: 'amex',
    },
    {
      date: '2024-12-14T00:00:00',
      description: "NANDO'S BRISTOL",
      notes: null,
      merchant_id: null,
      exclude_from_analytics: false,
      id: 'QrpcE8xvqNjsjtS8PH5rF2',
      amount: '384.38',
      category_id: 'TdTY9ahjNKanyAvyUCmUth',
      account_id: 'amex',
    },
    {
      date: '2024-12-12T00:00:00',
      description: 'UDEMY COURSE',
      notes: null,
      merchant_id: null,
      exclude_from_analytics: false,
      id: 'RspcF9xvqNjsjtS8PH5rF3',
      amount: '131.50',
      category_id: 'Q3enGA7mRz3zGE59edkhBB',
      account_id: 'amex',
    },
    {
      date: '2024-12-14T00:00:00',
      description: 'BOOTS PHARMACY',
      notes: null,
      merchant_id: null,
      exclude_from_analytics: false,
      id: 'StpcG0xvqNjsjtS8PH5rF4',
      amount: '104.43',
      category_id: 'nK9LfGwKsFpv87XY8FYLY2',
      account_id: 'amex',
    },
    {
      date: '2024-12-14T00:00:00',
      description: 'MAINTENANCE FEE',
      notes: null,
      merchant_id: null,
      exclude_from_analytics: false,
      id: 'TupcH1xvqNjsjtS8PH5rF5',
      amount: '12.99',
      category_id: '8dbxskvYv3k672TJCjniQx',
      account_id: 'amex',
    },
  ]

  private readonly demoAnalytics: AnalyticsResponse = {
    categories: [
      {
        id: 'Liwwdaqt7fPJ6LKFACjpiX',
        total: '2924.53',
      },
      {
        id: 'anXz4uDvzF29jzUqX7cyPq',
        total: '89.77',
      },
      {
        id: '3v2znBBbuK6aDTAkRdfsB6',
        total: '1234.64',
      },
      {
        id: 'nmvY3NerXM3t8n3GCD3S9e',
        total: '596.45',
      },
      {
        id: 'TZuwyBFHemk95U6avZfvEf',
        total: '518.25',
      },
      {
        id: 'TdTY9ahjNKanyAvyUCmUth',
        total: '384.38',
      },
      {
        id: 'Q3enGA7mRz3zGE59edkhBB',
        total: '131.50',
      },
      {
        id: 'nK9LfGwKsFpv87XY8FYLY2',
        total: '104.43',
      },
      {
        id: '8dbxskvYv3k672TJCjniQx',
        total: '12.99',
      },
    ],
    total: '5996.94',
  }

  async fetchTransactions(month?: string, showAll?: boolean): Promise<Transaction[]> {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    if (!showAll && month) {
      return this.demoTransactions.filter((transaction) => transaction.date.startsWith(month))
    }

    return this.demoTransactions
  }

  async fetchCategories(): Promise<Category[]> {
    await new Promise((resolve) => setTimeout(resolve, 300))
    return this.demoCategories
  }

  async fetchAnalytics(month?: string, showAll?: boolean): Promise<AnalyticsResponse> {
    await new Promise((resolve) => setTimeout(resolve, 400))

    if (!showAll && month) {
      // Calculate totals only for the specified month
      const monthlyTransactions = this.demoTransactions.filter((t) => t.date.startsWith(month))

      const categoryTotals = new Map<string | null, number>()
      let total = 0

      monthlyTransactions.forEach((transaction) => {
        const amount = parseFloat(transaction.amount)
        const categoryId = transaction.category_id

        categoryTotals.set(categoryId, (categoryTotals.get(categoryId) || 0) + amount)
        total += amount
      })

      return {
        categories: Array.from(categoryTotals.entries()).map(([id, total]) => ({
          id,
          total: total.toFixed(2),
        })),
        total: total.toFixed(2),
      }
    }

    return this.demoAnalytics
  }
}
