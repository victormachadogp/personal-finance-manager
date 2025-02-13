import { InjectionKey } from 'vue'
import { TransactionServiceInterface } from '../types/TransactionServiceInterface'
import { LiveTransactionService } from '../services/LiveTransactionService'
import { DemoTransactionService } from '../services/DemoTransactionService'

export const TransactionServiceKey: InjectionKey<TransactionServiceInterface> =
  Symbol('TransactionService')

export const createServiceProvider = (isDemoMode = false) => {
  const transactionService = isDemoMode
    ? new DemoTransactionService()
    : new LiveTransactionService()

  return {
    install(app: App) {
      app.provide(TransactionServiceKey, transactionService)
    },
  }
}
